import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    print("tqdm not installed, progress bar will not be shown")

    def tqdm(iterable, **kwargs):
        return iterable


class RepoVisibility(StrEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


@dataclass(frozen=True)
class RepoMetadata:
    name: str
    name_with_owner: str
    visibility: RepoVisibility
    default_branch_ref: str
    ssh_url: str
    url: str

    @classmethod
    def _from_json(cls, data: dict):
        data["default_branch_ref"] = data.pop("defaultBranchRef")["name"]
        data["name_with_owner"] = data.pop("nameWithOwner")
        data["ssh_url"] = data.pop("sshUrl")
        data["visibility"] = RepoVisibility(data.pop("visibility"))
        return cls(**data)


def fetch_repo_metadata(org, load_cache: bool, cache_file: Path):
    if load_cache:
        if not cache_file.exists():
            raise FileNotFoundError(f"Cache file {cache_file} does not exist - run with --do-update to fetch the repos")
        with open(cache_file, "r") as f:
            return [RepoMetadata._from_json(repo) for repo in json.load(f)]
    result = subprocess.run(
        [
            "gh",
            "repo",
            "list",
            org,
            "--limit",
            "1000",
            "--json",
            ",".join(  # noqa: FLY002
                (
                    "name",
                    "nameWithOwner",
                    "visibility",
                    "defaultBranchRef",
                    "sshUrl",
                    "url",
                )
            ),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    with open(cache_file, "w") as f:
        f.write(result.stdout)
    return [RepoMetadata._from_json(repo) for repo in json.loads(result.stdout)]


def clone_or_update_repo(repo: RepoMetadata, containing_dir: Path):
    repo_dir = containing_dir / repo.name
    if not repo_dir.exists():
        # clone the repo
        subprocess.run(["gh", "repo", "clone", repo.name_with_owner, repo_dir], check=True)
    else:
        # update the repo
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True, check=True, cwd=repo_dir
        ).stdout.strip()
        if current_branch != repo.default_branch_ref:
            subprocess.run(["git", "checkout", repo.default_branch_ref], check=True, cwd=repo_dir)
        subprocess.run(["git", "pull"], check=True, cwd=repo_dir, capture_output=True)


@dataclass(frozen=True)
class ArtifactIdentifier:
    group_id: str
    artifact_id: str
    version: str | None

    @property
    def id_(self):
        return f"{self.group_id}:{self.artifact_id}"

    @property
    def cid(self):
        return f"cluster_{self.group_id}:{self.artifact_id}"


@dataclass(frozen=True)
class PomArtifact:
    parent: ArtifactIdentifier | None
    identifier: ArtifactIdentifier
    name: str | None
    dependencies: list[ArtifactIdentifier]


def find_all_poms(workdir: Path):
    pom_files: list[Path] = []
    for root, dirs, files in workdir.walk():
        for file in files:
            if file == "pom.xml":
                pom_files.append(root / file)
    return pom_files


_RE_PROPERTY = re.compile(r"\$\{([^}]+)\}")


def _resolve_property(el: ET.Element | None, properties: dict[str, str]):
    if el is None:
        return None
    value = el.text
    if value is None:
        return None
    for match in _RE_PROPERTY.finditer(value):
        prop_name = match.group(1)
        if prop_name in properties:
            value = value.replace(match.group(0), properties[prop_name])
    return value


def _parse_artifact_identifier(
    elem: ET.Element, properties: dict[str, str], parent: ArtifactIdentifier | None = None
) -> ArtifactIdentifier:
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}

    group_id_elem = elem.find("m:groupId", ns)
    artifact_id_elem = elem.find("m:artifactId", ns)
    version_elem = elem.find("m:version", ns)

    group_id = _resolve_property(group_id_elem, properties) if group_id_elem is not None else None
    artifact_id = _resolve_property(artifact_id_elem, properties) if artifact_id_elem is not None else None
    version = _resolve_property(version_elem, properties) if version_elem is not None else None

    if parent is not None:
        if group_id is None:
            group_id = parent.group_id
        if version is None:
            version = parent.version

    assert group_id is not None
    assert artifact_id is not None
    return ArtifactIdentifier(
        group_id=group_id,
        artifact_id=artifact_id,
        version=version,
    )


def parse_pom(pom_file: Path) -> PomArtifact:
    tree = ET.parse(pom_file)
    root = tree.getroot()
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    properties: dict[str, str] = {}
    for prop in root.findall("m:properties/*", ns):
        assert prop.text is not None
        properties[prop.tag.split("}")[1]] = prop.text

    parent = None
    parent_elem = root.find("m:parent", ns)
    if parent_elem is not None:
        parent = _parse_artifact_identifier(parent_elem, properties)

    identifier = _parse_artifact_identifier(root, properties, parent=parent)
    assert identifier.artifact_id is not None
    assert identifier.group_id is not None
    assert identifier.version is not None
    assert "project.groupId" not in properties
    assert "project.version" not in properties
    assert "project.artifactId" not in properties
    properties["project.groupId"] = identifier.group_id
    properties["project.version"] = identifier.version
    properties["project.artifactId"] = identifier.artifact_id

    name_el = root.find("m:name", ns)
    name = _resolve_property(name_el, properties)

    dependencies = []
    for dep in root.findall("m:dependencies/m:dependency", ns):
        dependencies.append(_parse_artifact_identifier(dep, properties))

    return PomArtifact(parent=parent, identifier=identifier, name=name, dependencies=dependencies)


@dataclass
class GraphNode:
    name: str
    repositories: list[tuple(RepoMetadata, PomArtifact)]


class EdgeType(StrEnum):
    DEPENDS_ON = "DEPENDS_ON"
    CHILD_OF = "CHILD_OF"


@dataclass
class GraphEdge:
    version: list[tuple(RepoMetadata, str)]


@dataclass
class GraphHierarchy:
    main_artifact: PomArtifact | None
    contained_artifacts: list[PomArtifact] = field(default_factory=list)
    children: list["GraphHierarchy"] = field(default_factory=list)


def _dot_write_nodes(f, nodes: dict[str, GraphNode], color_overrides: dict[str, str] | None = None):
    for node_id, node in nodes.items():  # noqa: FURB122
        label = [
            f"<b>{node.name}</b>",
        ]
        if node.name != node_id:
            label.append(f"<font color='gray'>{node_id}</font>")
        if len(node.repositories) > 0:
            label.append(
                "<br/>".join(
                    [
                        f"{repo.name} ({repo.visibility})"
                        for repo, _ in sorted(node.repositories, key=lambda x: x[0].name)
                    ]
                )
            )
        color = color_overrides.get(node_id, "black") if color_overrides else "black"
        f.write(f'    "{node_id}" [label=<{'<br/>'.join(label)}>, shape=box, color="{color}"];\n')


def _dot_write_edges(f, edges: dict[(str, str, EdgeType), GraphEdge], color_overrides: dict[str, str] | None = None):
    for (from_id, to_id, edge_type), edge in edges.items():
        color = "black"
        if color_overrides:
            if to_id in color_overrides:
                color = color_overrides[to_id]
            elif from_id in color_overrides:
                color = color_overrides[from_id]
        style = "solid" if edge_type == EdgeType.DEPENDS_ON else "dashed"
        arrowhead = "normal" if edge_type == EdgeType.DEPENDS_ON else "empty"
        f.write(f'    "{from_id}" -> "{to_id}" [style="{style}", arrowhead="{arrowhead}", color="{color}"];\n')


def _dot_write_hierarchy(f, hierarchy: GraphHierarchy, indent: int = 1):
    _indent = "    " * indent
    _cindent = _indent + "    "
    # write subgraphs recursively
    if hierarchy.main_artifact is not None:
        f.write(f'{_indent}subgraph "{hierarchy.main_artifact.identifier.cid}" {{\n')
        name = (
            hierarchy.main_artifact.name
            if hierarchy.main_artifact.name is not None
            else hierarchy.main_artifact.identifier.artifact_id
        )
        f.write(f'{_cindent}label = <{name}<br/><font color="gray">{hierarchy.main_artifact.identifier.id_}</font>>;\n')
        f.write(f'{_cindent}style = "dashed";\n')
        f.write(f'{_cindent}color = "blue";\n')
        f.write(f'{_cindent}"{hierarchy.main_artifact.identifier.id_}" [color=blue];\n')
    for artifact in hierarchy.contained_artifacts:
        f.write(f'{_cindent}"{artifact.identifier.id_}";\n')
    for child_hierarchy in hierarchy.children:
        _dot_write_hierarchy(f, child_hierarchy, indent=indent + 1)
    if hierarchy.main_artifact is not None:
        f.write(f"{_indent}}}\n")


def create_dot_graph(
    poms: list[Path],
    artifacts: list[PomArtifact],
    repos_dict: dict[str, RepoMetadata],
    dot_file: str = "graph.dot",
    color_overrides: dict[str, str] | None = None,
):
    nodes: dict[str, GraphNode] = {}
    edges: dict[(str, str, EdgeType), GraphEdge] = {}
    root_hierarchy = GraphHierarchy(main_artifact=None, contained_artifacts=[], children=[])
    _hierarchies: dict[str, GraphHierarchy] = {}

    for pom_path, artifact in zip(poms, artifacts):
        id_ = artifact.identifier.id_
        name = artifact.name if artifact.name is not None else artifact.identifier.artifact_id
        # find the repo that contains this artifact
        repo_name = pom_path.parts[1]
        assert repo_name in repos_dict, f"Repo {repo_name} not found in fetched repos"
        repo = repos_dict[repo_name]
        if id_ not in nodes:
            nodes[id_] = GraphNode(name, [])
        assert nodes[id_].name == name, f"Conflicting names for {id_}: {nodes[id_].name} vs {name}"
        assert (repo, artifact) not in nodes[id_].repositories
        nodes[id_].repositories.append((repo, artifact))

        if artifact.parent is not None:
            key = (artifact.identifier.id_, artifact.parent.id_, EdgeType.CHILD_OF)
            if key not in edges:
                edges[key] = GraphEdge(version=[])
            edges[key].version.append((repo, artifact.identifier.version))

            if artifact.parent.id_ not in _hierarchies:
                _hierarchies[artifact.parent.id_] = GraphHierarchy(main_artifact=None)
            _hierarchies[artifact.parent.id_].contained_artifacts.append(artifact)

        for dep in artifact.dependencies:
            key = (artifact.identifier.id_, dep.id_, EdgeType.DEPENDS_ON)
            if key not in edges:
                edges[key] = GraphEdge(version=[])
            edges[key].version.append((repo, dep.version))

    # postprocess hierarchy children (as of now, just the direct child nodes were added, still need to fill in the main node and children)
    for artifact in artifacts:
        if artifact.identifier.id_ in _hierarchies:
            hierarchy = _hierarchies[artifact.identifier.id_]
            hierarchy.main_artifact = artifact
            if artifact.parent is not None:
                assert artifact.parent.id_ in _hierarchies
                parent_hierarchy = _hierarchies[artifact.parent.id_]
            else:
                parent_hierarchy = root_hierarchy
            if hierarchy not in parent_hierarchy.children:
                parent_hierarchy.children.append(hierarchy)

    # only keep edges with both nodes present in the graph, i.e. remove external dependencies
    edges = {k: v for k, v in edges.items() if k[0] in nodes and k[1] in nodes}

    with open(dot_file, "w") as f:
        f.write("digraph G {\n")
        _dot_write_nodes(f, nodes, color_overrides)
        _dot_write_edges(f, edges, color_overrides)
        _dot_write_hierarchy(f, root_hierarchy)
        f.write("}\n")

    for tool in [
        "dot",
        # "fdp",
    ]:
        subprocess.run([tool, "-Tsvg", dot_file, "-o", f"graph-{tool}.svg"], check=True)
        subprocess.run([tool, "-Tpdf", dot_file, "-o", f"graph-{tool}.pdf"], check=True)


def main():
    args = argparse.ArgumentParser(
        description="Generate a graph of the TLS-Attacker repositories and their dependencies"
    )
    args.add_argument(
        "--do-update",
        action="store_true",
        help="Fetch the repositories (fetches metadata and clones/updates the repos; requires gh cli to be installed and authenticated)",
    )
    args.add_argument(
        "--org",
        type=str,
        default="tls-attacker",
        help="GitHub organization to fetch repos from; only used if --do-update is set",
    )
    args.add_argument("--workdir", type=str, default="tmp", help="Directory to clone/update the repositories in")
    args = args.parse_args()
    workdir = Path(args.workdir)

    repos = fetch_repo_metadata(args.org, load_cache=not args.do_update, cache_file=workdir / "repos.json")
    repos_dict = {repo.name: repo for repo in repos}
    print(f"Found {len(repos)} repos")

    if args.do_update:
        for repo in tqdm(repos, desc="Cloning/updating repos", dynamic_ncols=True):
            clone_or_update_repo(repo, workdir)

    poms = find_all_poms(workdir)
    print(f"Found {len(poms)} pom.xml files")
    artifacts = list(map(parse_pom, poms))
    create_dot_graph(
        poms,
        artifacts,
        repos_dict,
        color_overrides={
            "de.rub.nds:protocol-toolkit-bom": "gray",
            "de.rub.nds:modifiable-variable": "#5e8556",
            "de.rub.nds.tls.attacker:tls-core": "#856936",
            "de.rub.nds.tls.attacker:transport": "#81802f",
        },
    )


if __name__ == "__main__":
    main()
