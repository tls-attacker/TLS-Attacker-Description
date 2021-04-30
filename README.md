<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [TLS-Attacker-Description](#tls-attacker-description)
- [Project Structure](#project-structure)
  - [Modifiable Variable](#modifiable-variable)
  - [ASN.1-Tool](#asn1-tool)
  - [X.509-Attacker](#x509-attacker)
  - [TLS-Attacker](#tls-attacker)
  - [TLS-Scanner](#tls-scanner)
- [Installation](#installation)
  - [Stable Versions](#stable-versions)
  - [Development Versions/Snapshots](#development-versionssnapshots)
- [Committing to the project](#committing-to-the-project)
  - [Repositories](#repositories)
  - [Branches](#branches)
  - [Tests](#tests)
  - [License Headers](#license-headers)
  - [Code Style](#code-style)
  - [Pull Requests](#pull-requests)
- [The build pipeline / Jenkins](#the-build-pipeline--jenkins)
  - [Viewing And Changing Jobs](#viewing-and-changing-jobs)
  - [Maintaining Jenkins](#maintaining-jenkins)
- [Snapshot Repository / Nexus](#snapshot-repository--nexus)
  - [Setup](#setup)
  - [Maintaining Nexus](#maintaining-nexus)
- [Server Architecture / Nginx](#server-architecture--nginx)
- [Deploying to Nexus And Maven Central](#deploying-to-nexus-and-maven-central)
- [FAQ](#faq)
  - [I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development](#i-made-a-change-to-x509-attacker-development-and-it-does-not-show-up-in-tls-attacker-development)
  - [I am getting XSD validation errors during a WorkflowTrace copy operation](#i-am-getting-xsd-validation-errors-during-a-workflowtrace-copy-operation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# TLS-Attacker-Description

![licence](https://img.shields.io/badge/License-Apachev2-brightgreen.svg)
[![Build Status](https://hydrogen.cloud.nds.rub.de/buildStatus/icon.svg?job=TLS-Attacker-Description)](https://hydrogen.cloud.nds.rub.de/job/TLS-Attacker-Description/)


This repository contains additional resources for the TLS-Attacker project. Here you can find information about installation, committing to repositories, the project structure, and more. This repository is also contains information about project-internal infrastructure to help everyone be on the same page.

# Project Structure

The main structure of the TLS-Attacker project consists of the following 5 sub-projects. An arrow from e.g. ASN.1-Tool to ModifiableVariable indicates that ASN.1-Tool requires ModifiableVariable as a dependency.

![TLS-Attacker Structure](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/structure.png)

We can see that while Modifiable Variable requires no other sub-project from the TLS-Attacker-Project, TLS-Scanner requires all of them. For an installation reference see [Installation](#Installation).

Most repositories in the TLS-Attacker-Project have a public and a development repository. The development repositories can only be seen by committers such as students or employees and are the location to make pull requests. This way, research results and exploits are not leaked to the public. The public repositories can be seen by anyone and are updated every once in a while with stable versions of the development repositories.

## Modifiable Variable

Public/Development: https://github.com/tls-attacker/ModifiableVariable

Modifiable variable allows one to set modifications to basic types after or before their values are actually determined. When their actual values are determined and one tries to access the value via getters, the original value will be returned in a modified form accordingly.

The concept of modifiable variables is directly or indirectly used by all other sub-projects in the TLS-Attacker-Project.

## ASN.1-Tool

Public: https://github.com/tls-attacker/ASN.1-Tool

Development: https://github.com/tls-attacker/ASN.1-Tool-Development

ASN.1 Tool is an open-source framework for generating arbitrary ASN.1 structures. The tool also provides mechanisms to define modifications of original ASN.1 values. Resulting binary ASN.1 structures can then be used for further processing in other tools.

The tool is not intended to be used directly, but by other software projects (such as the TLS-Attacker-Project) as a library.

## X.509-Attacker

Public: https://github.com/tls-attacker/X509-Attacker

Development: https://github.com/tls-attacker/X509-Attacker-Development

X.509-Attacker is a tool based on ASN.1 Tool for creating arbitrary certificates; including especially invalid and malformed certificates. Since X.509 certificates encode their contents in ASN.1, this tool extends the features of the ASN.1 Tool in terms of certificate signing. Also, X.509-Attacker introduces a feature of referencing XML elements in order to avoid redundancies when defining certificates in XML.

While X.509-Attacker can be used on its own, the [TLS-Attacker](#tls-attacker) sub-project uses it as a dependency to create certificates in TLS handshakes.

## TLS-Attacker

Public: https://github.com/tls-attacker/TLS-Attacker

Development: https://github.com/tls-attacker/TLS-Attacker-Development

TLS-Attacker is a Java-based framework for analyzing TLS libraries. It is able to send arbitrary protocol messages in an arbitrary order to the TLS peer, and define their modifications using a provided interface. This gives the developer an opportunity to easily define a custom TLS protocol flow and test it against his TLS library.

This presents the main tool of the TLS-Attacker-Project, which can send arbitrary messages to servers and execute predefined attacks. TLS-Attacker has the following submodules: TLS-Core, Utils, Attacks, Transport, TraceTool, TLS-Client, TLS-Mitm, TLS-Attacker, TLS-Server, TLS-Forensics. Check the repository's [ReadMe](https://github.com/tls-attacker/TLS-Attacker) for more details on the submodules.

## TLS-Scanner

Public: https://github.com/tls-attacker/TLS-Scanner

Development: https://github.com/tls-attacker/TLS-Scanner-Development

TLS-Scanner uses TLS-Attacker to test a specific server against multiple known vulnerabilities of TLS-Servers. In the end, TLS-Scanner assigns a score attributing the security of said server. Furthermore, it offers a list of recommendations that increase the security of the server. Test vectors range from key length to known attacks such as Heartbleed

# Installation

You can either work on the stable versions or on the development/Snapshot versions of the TLS-Attacker project. While the former are... well, stable the latter usually include more functionality. Also, if you want to later [commit](#committing-to-the-project) to those repositories you have to use the development versions anyways.

## Stable Versions

The TLS-Attacker-Project uses Maven as a build tool. All stable versions of the sub-projects are accessible via Maven Central and can be included as dependencies in your projects pom.xml. An example for the X.509-Attacker is given below.

```xml
<!-- https://mvnrepository.com/artifact/de.rub.nds/X509Attacker -->
<dependency>
    <groupId>de.rub.nds</groupId>
    <artifactId>X509Attacker</artifactId>
    <version>1.1.0</version>
</dependency>
```
You can also view the TLS-Attacker-Project artifacts on [Maven Central](https://mvnrepository.com/artifact/de.rub.nds).

If you want to install a runnable jar (for example the TLS-Scanner sub-project to scan your server) you can install it manually from GitHub. An example for the TLS-Scanner would be

```bash
$ git clone https://github.com/tls-attacker/TLS-Scanner.git
$ cd TLS-Scanner
$ mvn clean install
```
All internal dependencies are resolved by Maven using the Maven central repository.

The jar files are accessible in the "apps" folder. If you want to copy the jar files remember to copy the "apps/lib" folder as well, it contains the dependencies of the final jar.

## Development Versions/Snapshots

The compiled "Snapshot" jars from the development repositories are not uploaded to Maven Central. You either have to download all sub-projects from GitHub and install them manually or you can download them from the Nexus Snapshot repository. 

For manual installation you have to install all sub-projects as follows.

```bash
$ git clone https://github.com/tls-attacker/ModifiableVariable.git
$ cd ModifiableVariable
$ mvn clean install
$ cd ../
$ git clone https://github.com/tls-attacker/ASN.1-Tool-Development.git
$ cd ASN.1-Tool
$ mvn clean install
$ cd ../
$ git clone https://github.com/tls-attacker/X509-Attacker-Development.git
$ cd X509-Attacker
$ mvn clean install
$ cd../
$ git clone https://github.com/tls-attacker/TLS-Attacker-Development.git
$ cd TLS-Attacker
$ mvn clean install
$ cd ../
$ git clone https://github.com/tls-attacker/TLS-Scanner-Development.git
$ cd TLS-Scanner
$ mvn clean install
```

Beware that you will have to install all sub-projects again if you want any changes to take effect.

For the installation via the Nexus Snapshot Repository you have to [set up your access to the repository](#snapshot-repository--nexus). With that done, Maven can find them as if they were on the Maven Central repository.

You can include them as dependencies in your project using

```xml
<!-- https://mvnrepository.com/artifact/de.rub.nds/X509Attacker -->
<dependency>
    <groupId>de.rub.nds</groupId>
    <artifactId>X509Attacker</artifactId>
    <version>1.2.0-SNAPSHOT</version>
</dependency>
```

and install the jars with

```bash
$ git clone https://github.com/tls-attacker/TLS-Scanner-Development.git
$ cd TLS-Scanner
$ mvn clean install
```

# Committing to the project

Different people commit to the repository for different reasons and with different ambitions. To keep the code base somewhat uniform and readable for everyone we introduced a few guidelines.

## Repositories

Most sub-projects of the TLS-Attacker-Project have a stable public repository and a private repository which holds the development version. Please use the private/development repositories when committing code or opening issues.

## Branches

The development repositories contain a master branch and several feature branches. Directly pushing to the master branch is not possible. If you want to work on a new feature or fix a bug (maybe from an issue you opened) simply create a new branch from the master branch. 

```bash
$ git checkout master
$ git checkout -b <your branch>
```

You can also create a new branch from any other branch than the master branch but remember that that can lead to a more complicating merging process later on.

## Tests

Each sub-project in the TLS-Attacker-Project has a set of Unit tests. Each of them has to pass before your change or feature can be merged into the master branch. In the TLS-Attacker and TLS-Scanner sub-project, some tests are responsible for generating config and resource files. Therefore, we do not recommend skipping tests too often. However, we recommend writing tests should you add substantial features to the code base.

## License Headers

License Headers in each sub-project are added automatically by the `license-maven-plugin` during installation. You can also check if all license headers are correct with

```bash
$ mvn license:check
```

and update them manually using

```bash
$ mvn license:format
```

All license headers have to be up to date before your change or feature can be merged into the master branch.

If you want to change the formatting of the license header you can change the `license_header_plain.txt` in each repository. If you want to change the values of the license header you can set them in the properties of the `license-maven-plugin`.


## Code Style

Code Styling is split into two parts. The `formatter-maven-plugin` handles visual formatting such as line breaks and white spaces as specified in the `maven-eclipse-codestyle.xml`. The visual formatting is performed automatically by Maven during an installation. You can also check if the formatting is correct with

```bash
$ mvn formatter:validate
```

and format manually using

```bash
$ mvn formatter:format
```
The visual formatting is required before your change or feature can be merged into the master branch.

More refined code style rules are defined in `checkstyle.xml`. These rules are similar to the Google Java Style. They can not be applied by Maven or your IDE but your IDE can detect them using an appropriate Checkstyle plugin. 

To use the refined code style rules in IntelliJ, you would first need to install the `CheckStyle-IDEA` plugin. Under Settings->Tools->Checkstyle you can add the `checkstyle.xml` as a configuration file. Under Settings->Editor->Inspections you can enable and disable the custom inspections. Inspections can be run via Analyze->Inspect Code.

The `maven-eclipse-codestyle.xml` is exported from Eclipse. The easiest way to make substantial changes to it is by importing it to Eclipse, make the changes there, and exporting it again. The `checkstyle.xml` is a slightly modified version of the [Google Java Style checkstyle](https://github.com/checkstyle/checkstyle/blob/master/src/main/resources/google_checks.xml). You can directly modify it according to the [Checkstyle documentation](http://checkstyle.org).

## Pull Requests

Merging your changes into the master branch can be done via a pull request. To this end, simply open a pull request from your branch into the master branch via Github. 

The [Jenkins build pipeline](#the-build-pipeline--jenkins) will test and compile your pull request and checks whether [license headers](#license-headers) and the [visual formatting](#code-style) is up to date. If any of the checks fail Jenkins will tell you on your pull request. Unfortunately, due to disclosure policies, only maintainers are allowed to see the specific compilation or check error. However, they must review your pull requests anyways and can hint you in the right direction. Any fixes or changes you commit to your branch will be included in your pull request and checked again by Jenkins.

Before your change or fix can be merged into the master branch, a maintainer has to approve your pull request. Before they do so, they might give you feedback in the form of comments on your pull requests. After you resolved the feedback (or asked questions on the feedback) a maintainer will review your pull request again. This process is repeated until the pull request is finally merged.

If you want a specific maintainer to review your pull request (maybe your thesis advisor), you can request one on GitHub. You can also mention other users in your pull request if you believe they can help with something or would be interested in your change/fix.

We know it can take some time until your pull request might be merged, but please be patient :)

# The build pipeline / Jenkins

All sub-projects of the TLS-Attacker project have (or should have) a corresponding build pipeline. The pipeline is responsible for testing, validating, and compiling all commits and pull request of the sub-project. With a set up build pipeline, each correct and successfully commit on every branch will be marked with a green checkmark. All non-passing commits will be marked with a red cross. The same is done to the commits of any open pull request. Furthermore, the compilation status of each sub-project is indicated by a badge in the ReadMe. You can see this in this repository as well.

A sub-project will also be checked by the build pipeline if any of its dependency sub-projects received a change.

## Viewing And Changing Jobs

The build pipeline is managed by a Jenkins server accessible at https://hydrogen.cloud.nds.rub.de/. Here you can view and edit jobs. Once you selected a job you can view the console output of a build via BuildHistory(#job)->ConsoleOutput. Under Configure, you can change the settings of the job.

You can also create a new job in Jenkins using the "New Item" option in the main menu. We recommend to insert one of the already present Jenkins jobs into the "Copy from" setting. That way, you only have to change the repository link to receive an already working Jenkins job. 

When creating a new Job for a sub-project, make sure to create a webhook with the following properties under GitHub-Project->Settings->Webhooks

![GitHub webhook](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/webhook.JPG)

The build badge for your ReadMe is accessible via \<Your Job\>->"Embeddable Build Status"->Markdown->unprotected. Be sure to replace http:// with https://.

The correct "Source Code Management" credentials for the repository are "NDS-JENKINS/****** (Github login)". 

TODO: ssh hickups when adding a node, further unintuitive settings for new jobs?

## Maintaining Jenkins

Under "Manage Jenkins", you can view and change access rights, manage plugins, and change Jenkins' internal settings.

Under "configure System", you can change the settings of the Jenkins plugins. Important settings are the "Github Token" as a credential under "Github" and "GitHub Pull Request Builder", the "Slack Token" as a credential under "Slack", and the Admin list under "GitHub Pull Request Builder. If a user is not specified in the Admin list and not part of an organization in the Admin list their pull request will not be build.

Under "Global Tool Configuration", you can add JDK installations, change Maven settings, and add Maven installations. Any new JDK installations or settings files you want to add have to be present on the machine that Jenkins runs on. See [Server Architecture](#server-architecture--nginx) for that.

Under "Manage Plugins", you can install, update, and remove plugins. 

Under "Configure Global Security", you can edit the access rights for different users. The "anonymous" user refers to every user that is not logged in into Jenkins. It needs the "View Status" authorization for the GitHub Build Status plugin. Currently, the anonymous user has no read authorization due to disclosure issues.

Under "Manage Credentials", you can manage and add Tokens used by different Plugins to authenticate to third party services.

Under "Manage Users" you can add or remove users that have potential access rights to the Jenkins server

Jenkins itself must be updated via the apt package manager on the virtual machine Jenkins is running on. See [Server Architecture](#server-architecture--nginx) for information on connecting to the virtual machine.

# Snapshot Repository / Nexus

As mentioned in [Installation](#installation), we provide a Nexus Snapshot Repository. It contains Snapshot versions of most sub-projects of the TLS-Attacker Project. Currently, only the maven-snapshots repository is used as all stable builds are pushed to the Maven Central repository.

## Setup

To keep the Snapshot versions of the TLS-Attacker project under disclosure, only members of the GitHub organization "TLS-Attacker" are allowed to use it. To provide authentication, you must a GitHub personal access token with the read:org Scope selected (https://github.com/settings/tokens/new)

![GitHub token](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/token.JPG)

After generation, be sure to copy the token. You will need it during the next step.

Next, open your Maven settings.xml. You can usually find it under `${user.home}/.m2/settings.xml`. If you're still confused you can run `mvn -X` and wait for Maven to tell your the location or access the settings file via your favorite IDE. (In IntelliJ: pom.xml->Context Menu->Maven->Open 'settings.xml')

Add the following server and profile to your `.settings.xml`, replacing "GitHub Personal Access Token" with the token you created earlier and "Username" with your GitHub username.

```xml
<servers>
        <server>
            <id>rub-nexus</id>
            <username>"Username"</username>
            <password>"GitHub Personal Access Token"</password>
        </server>
    </servers>
    <profiles>
        <profile>
            <id>TLS-Attacker</id>
            <repositories>
                <repository>
                    <id>default</id>
                    <name>Maven Central</name>
                    <url>https://repo1.maven.org/maven2/</url>
                </repository>
                <repository>
                    <id>rub-nexus</id>
                    <name>TLS-ATTACKER SNAPSHOTS</name>
                    <url>https://hydrogen.cloud.nds.rub.de/nexus/repository/maven-public/</url>
                </repository>
            </repositories>
        </profile>
    </profiles>
    <activeProfiles>
        <activeProfile>TLS-Attacker</activeProfile>
    </activeProfiles>
```

Maven will now download all Snapshot dependencies from the Nexus Snapshot Repository.

## Maintaining Nexus

The Nexus server settings can be accessed through https://hydrogen.cloud.nds.rub.de/nexus/#admin/repository. Here you can manage repositories, add cleanup policies, content selectors, routing rules, and access rights.

Having a cleanup policy is advised as the Snapshot Repository should not occupy the entire storage space of the virtual machine.

User authentication on the Nexus server is done via a [GitHub oauth plugin](https://github.com/L21s/nexus3-github-oauth-plugin). It allows users to log on to the Nexus server with their GitHub username and an oauth token by mapping their GitHub teams to Nexus Roles. To allow users of a GitHub team to access the Nexus servers with certain privileges, there has to be a Role in Nexus with the corresponding name. 

Consider the following: There exists a team named "bachelor-students" in the GitHub group "TLS-Attacker". We not want to give all users in this team read access to the Snapshot repository to allow them to download packages via Maven. However, we want to prevent them from uploading anything into the repository or making administrative changes. The corresponding role would look as follows.

![Nexus Roles](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/nexus_roles.JPG)

Instead of inheriting from the Viewer-Role, we could also give them the following privileges manually:
- nx-healthcheck-read
- nx-repository-view-*-*-browse
- nx-repository-view-*-*-read
- nx search-read

The privileges can be managed in the Privileges tab of Nexus using the following documentation https://help.sonatype.com/repomanager3/system-configuration/access-control/privileges.

# Server Architecture / Nginx

# Deploying to Nexus And Maven Central

# FAQ

## I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development

For the changes to take effect you have to manually install both X.509-Attacker and the TLS-Attacker sub-project. The Snapshot repository only contains the compiled master branches of the development sub-projects.

## I am getting XSD validation errors during a WorkflowTrace copy operation

It is likely that your resource files are out of date. Try running `mvn test` to update your XSD and config files.