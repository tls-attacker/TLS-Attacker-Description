<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [TLS-Attacker-Description](#tls-attacker-description)
- [Project Structure](#project-structure)
  - [Modifiable Variable](#modifiable-variable)
  - [ASN.1-Attacker](#asn1-attacker)
  - [X.509-Attacker](#x509-attacker)
  - [TLS-Attacker](#tls-attacker)
  - [TLS-Scanner](#tls-scanner)
  - [TLS-Crawler](#tls-crawler)
  - [TLS-State-VulnerabilityFinder](#tls-state-vulnerabilityfinder)
  - [TLS-Docker-Library](#tls-docker-library)
- [Installation](#installation)
  - [Stable Versions](#stable-versions)
  - [Development Versions/Snapshots](#development-versionssnapshots)
- [Committing to the project](#committing-to-the-project)
  - [Repositories](#repositories)
  - [Branches](#branches)
  - [Tests](#tests)
  - [License Headers](#license-headers)
  - [Code Style](#code-style)
  - [Logging](#logging)
  - [Pull Requests](#pull-requests)
- [The build pipeline / Jenkins](#the-build-pipeline--jenkins)
  - [Viewing And Changing Jobs](#viewing-and-changing-jobs)
  - [Maintaining Jenkins](#maintaining-jenkins)
- [Snapshot Repository / Nexus](#snapshot-repository--nexus)
  - [Setup](#setup)
  - [Maintaining Nexus](#maintaining-nexus)
  - [Docker Repository](#docker-repository)
- [Server Architecture / Nginx](#server-architecture--nginx)
  - [Nginx Configuration](#nginx-configuration)
  - [Maven Configuration](#maven-configuration)
- [Deploying to Nexus And Maven Central](#deploying-to-nexus-and-maven-central)
  - [Prerequisites for Nexus](#prerequisites-for-nexus)
  - [Setting up Maven Central](#setting-up-maven-central)
- [FAQ](#faq)
  - [I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development](#i-made-a-change-to-x509-attacker-development-and-it-does-not-show-up-in-tls-attacker-development)
  - [I am getting XSD validation errors during a WorkflowTrace copy operation](#i-am-getting-xsd-validation-errors-during-a-workflowtrace-copy-operation)
  - [Is there a demo server that I can attack?](#is-there-a-demo-server-that-i-can-attack)
  - [I need to build a project frequently but executing the tests takes very long](#i-need-to-build-a-project-frequently-but-executing-the-tests-takes-very-long)
  - [I did not find my problem or question. Where can I ask for help?](#i-did-not-find-my-problem-or-question-where-can-i-ask-for-help)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# TLS-Attacker-Description

![licence](https://img.shields.io/badge/License-Apachev2-brightgreen.svg)
[![Build Status](https://hydrogen.cloud.nds.rub.de/buildStatus/icon.svg?job=TLS-Attacker-Description)](https://hydrogen.cloud.nds.rub.de/job/TLS-Attacker-Description/)


This repository contains additional resources for the TLS-Attacker project. Here you can find information about installation, committing to repositories, the project structure, and more. This repository is also contains information about project-internal infrastructure to help everyone be on the same page.

# Project Structure

The main structure of the TLS-Attacker project consists of the following 5 sub-projects. An arrow from e.g. ASN.1-Attacker to ModifiableVariable indicates that ASN.1-Attacker requires ModifiableVariable as a dependency.

![TLS-Attacker Structure](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/structure.png)

We can see that while Modifiable Variable requires no other sub-project from the TLS-Attacker-Project, TLS-Scanner requires all of them. For an installation reference see [Installation](#Installation).

Most repositories in the TLS-Attacker-Project have a public and a development repository. The development repositories can only be seen by committers such as students or employees and are the location to make pull requests. This way, research results and exploits are not leaked to the public. The public repositories can be seen by anyone and are updated every once in a while with stable versions of the development repositories.

## Modifiable Variable

Public/Development: https://github.com/tls-attacker/ModifiableVariable

Modifiable variable allows one to set modifications to basic types after or before their values are actually determined. When their actual values are determined and one tries to access the value via getters, the original value will be returned in a modified form accordingly.

The concept of modifiable variables is directly or indirectly used by all other sub-projects in the TLS-Attacker-Project.

## ASN.1-Attacker

Public: https://github.com/tls-attacker/ASN.1-Attacker

Development: https://github.com/tls-attacker/ASN.1-Attacker-Development

ASN.1-Attacker is an open-source framework for generating arbitrary ASN.1 structures. The tool also provides mechanisms to define modifications of original ASN.1 values. The resulting binary ASN.1 structures can then be used for further processing in other tools.

The tool is not intended to be used directly, but by other software projects (such as the TLS-Attacker-Project) as a library.

## X.509-Attacker

Public: https://github.com/tls-attacker/X509-Attacker

Development: https://github.com/tls-attacker/X509-Attacker-Development

X.509-Attacker is a tool based on ASN.1-Attacker for creating arbitrary certificates; including especially invalid and malformed certificates. Since X.509 certificates encode their contents in ASN.1, this tool extends the features of the ASN.1 Tool in terms of certificate signing. Also, X.509-Attacker introduces a feature of referencing XML elements in order to avoid redundancies when defining certificates in XML.

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

## TLS-Crawler

Public/Development: https://github.com/tls-attacker/TLS-Crawler

TLS-Crawler uses TLS-Scanner to test multiple server on the internet against multiple known vulnerabilities. It does so in parallel and saves a server's score and a detailed report in a database. This project is currently undergoing changes from a command line based program to a docker based and maybe permanently-running service to allow for easier load-balancing between student-scans.

## TLS-State-VulnerabilityFinder

Development: https://github.com/tls-attacker/TLS-StateVulnFinder

TLS-State-VulnerabilityFinder utilizes state learning to learn the state machine of an arbitrary tls-server. To this end, it sends tls messages from the Tls-Attacker to the server. This repository is currently undergoing development to include server- and client-scanning with multiple tls versions and extensions.

## TLS-Docker-Library

The TLS-Docker-Library can build and run multiple open-source tls servers as docker containers. For building, it provides a python script while for running the project reuqires java. The built docker images are also saved in a nexus repository to negate the need for building images yourself (see [Docker Repository](#docker-repository)).

# Installation

You can either work on the stable versions or on the development/Snapshot versions of the TLS-Attacker project. While the former are... well, stable the latter usually include more functionality. Also, if you want to later [commit](#committing-to-the-project) to those repositories you have to use the development versions anyways.

## Stable Versions

The TLS-Attacker-Project uses Maven as a build tool. All stable versions are first deployed to [the internal Nexus repository](#snapshot-repository--nexus) and all versions required for public releases are also deployed to Maven Central. Stable versions can be included as dependencies in your projects pom.xml. An example for the X.509-Attacker is given below.

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
$ git clone https://github.com/tls-attacker/ASN.1-Attacker-Development.git
$ cd ASN.1-Attacker-Development
$ mvn clean install
$ cd ../
$ git clone https://github.com/tls-attacker/X509-Attacker-Development.git
$ cd X509-Attacker-Development
$ mvn clean install
$ cd../
$ git clone https://github.com/tls-attacker/TLS-Attacker-Development.git
$ cd TLS-Attacker-Development
$ mvn clean install
$ cd ../
$ git clone https://github.com/tls-attacker/TLS-Scanner-Development.git
$ cd TLS-Scanner-Development
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

## Logging

To get better performance in TLS Attacker, we use lazzy logging. This means that when we need to add parameters to a log statement, we use the following logging:

```java
LOGGER.debug("Log: {}", value);
```

If we have a ByteArray, we could use the ByteArray as a parameter. The logging layout replaces the ByteArray with a HexString.

```java
LOGGER.debug("Log: {}", byteArray);
```

In case we need to calculate something before logging, it is best to use a lamda expression. 

```java
LOGGER.debug("Log: {}", () -> value.calculateSomething());
```

The reason for the better performance is that the calculation of the value is only performed when the log level is printed. So we get up to 500x faster performance if we do not calculate the string for a ByteArray in the log statement, as in the following example. 

```java
//Do not log bytes Array like this!
LOGGER.debug("Log: {}", ArrayConverter.bytesToHexString(byteArray));
```

In the `log4j2.xml` it is possible to set prettyPrinting or an initialNewLine. For this the parameters `prettyPriniting` and `initNewLine` can be given to the `ExtendedPatternLayout`.

In the following example prettyPrinting is used, which starts with a new line before the output of the byte array:

```xml
<ExtendedPatternLayout pattern="%highlight{%d{HH:mm:ss}{GMT+0} [%t] %-5level: %c{1} - %msg%n%throwable}" prettyPrinting="true" initNewLine="false"/>
```

## Pull Requests

Merging your changes into the master branch can be done via a pull request. To this end, simply open a pull request from your branch into the master branch via Github. 

The [Jenkins build pipeline](#the-build-pipeline--jenkins) will test and compile your pull request and checks whether [license headers](#license-headers) and the [visual formatting](#code-style) is up to date. If any of the checks fail Jenkins will tell you on your pull request. Unfortunately, due to disclosure policies, only maintainers are allowed to see the specific compilation or check error. However, they must review your pull requests anyways and can hint you in the right direction. Any fixes or changes you commit to your branch will be included in your pull request and checked again by Jenkins.

Before your change or fix can be merged into the master branch, a maintainer has to approve your pull request. Before they do so, they might give you feedback in the form of comments on your pull requests. After you resolved the feedback (or asked questions on the feedback) a maintainer will review your pull request again. This process is repeated until the pull request is finally merged.

If you want a specific maintainer to review your pull request (maybe your thesis advisor), you can request one on GitHub. You can also mention other users in your pull request if you believe they can help with something or would be interested in your change/fix.

We know it can take some time until your pull request might be merged, but please be patient :)

# The build pipeline / Jenkins

All sub-projects of the TLS-Attacker project have (or should have) a corresponding build pipeline. The pipeline is responsible for testing, validating, and compiling all commits and pull request of the sub-project. With a set up build pipeline, each correct and successfully commit on every branch will be marked with a green checkmark. All non-passing commits will be marked with a red cross. The same is done to the commits of any open pull request. Furthermore, the compilation status of each sub-project is indicated by a badge in the ReadMe. You can see this in this repository as well.

A sub-project will also be checked by the build pipeline if any of its dependency sub-projects received a change.

All commits made by Jenkins are done through the distinguished GitHub user 'NDS-Jenkins'.

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

As mentioned in [Installation](#installation), we provide an internal Nexus Repository for snapshots and internal releases. This section describes how to configure Maven and Docker to use the repository.

## Setup

To keep the SNAPSHOT and internal release versions of the TLS-Attacker project under disclosure, only members of the GitHub organization "TLS-Attacker" are allowed to use it, and you need to be given access rights by one of the Administrators. 

Once you have credentials, open your Maven settings.xml. You can usually find it under `${user.home}/.m2/settings.xml`. If you're still confused, you can run `mvn -X` and wait for Maven to tell you the location or access the settings file via your favorite IDE. (In IntelliJ: pom.xml->Context Menu->Maven->Open 'settings.xml')

Add the following server and profile to your `settings.xml`, replacing `nexus_password` (within `<password>`) with the provided password and `nexus_username` (within `username`) with your nexus username.

```xml
<settings>
    <servers>
        <server>
            <id>rub-nexus</id>
            <username>nexus_username</username>
            <password>nexus_password</password>
        </server>
    </servers>
    <profiles>
        <profile>
            <id>protocol-attacker</id>
            <repositories>
                <repository>
                    <id>rub-nexus</id>
                    <name>Nexus Internal Repository</name>
                    <url>https://hydrogen.cloud.nds.rub.de/nexus/repository/maven-public/</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>always</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>true</enabled>
                        <updatePolicy>always</updatePolicy>
                    </snapshots>
                </repository>
            </repositories>
        </profile>
    </profiles>
    <!-- This section is optional but recommended to reduce load on the maven central servers -->
    <mirrors>
        <mirror>
            <id>rub-nexus</id>
            <name>Nexus Interal Repository (Maven Central Mirror)</name>
            <url>https://hydrogen.cloud.nds.rub.de/nexus/repository/maven-central/</url>
            <mirrorOf>central,!central-upload</mirrorOf>
        </mirror>
    </mirrors>
    <activeProfiles>
        <activeProfile>protocol-attacker</activeProfile>
    </activeProfiles>
</settings>
```

Maven will now download all dependencies and plugins from the internal Nexus Repository.

## Maintaining Nexus

The Nexus server settings can be accessed through https://hydrogen.cloud.nds.rub.de/nexus/#admin/repository. Here you can manage repositories, add cleanup policies, content selectors, routing rules, and access rights.

Having a cleanup policy is advised as the Snapshot Repository should not occupy the entire storage space of the virtual machine.

User authentication on the Nexus server is done via a [GitHub oauth plugin](https://github.com/L21s/nexus3-github-oauth-plugin). It allows users to log on to the Nexus server with their GitHub username and a GitHub personal access token by mapping their GitHub teams to Nexus Roles. To allow users of a GitHub team to access the Nexus servers with certain privileges, there has to be a Role in Nexus with the corresponding name. 

Consider the following: There exists a team named "bachelor-students" in the GitHub group "TLS-Attacker". We not want to give all users in this team read access to the Snapshot repository to allow them to download packages via Maven. However, we want to prevent them from uploading anything into the repository or making administrative changes. The corresponding role would look as follows.

![Nexus Roles](https://github.com/tls-attacker/TLS-Attacker-Description/blob/master/resources/figures/nexus_roles.JPG)

Instead of inheriting from the Viewer-Role, we could also give them the following privileges manually:
- nx-healthcheck-read
- nx-repository-view-*-*-browse
- nx-repository-view-*-*-read
- nx search-read

The privileges can be managed in the Privileges tab of Nexus using the following documentation https://help.sonatype.com/repomanager3/system-configuration/access-control/privileges.

## Docker Repository

The Nexus server also hosts a Docker repository which can be accessed under https://hydrogen.cloud.nds.rub.de. When logging on to the repository using `docker login https://hydrogen.cloud.nds.rub.de` you have to provide credentials. These are your nexus credentials that are provided by us during the [Setup](#snapshot-repository--nexus). After logging on to the repository, you can pull docker images, e.g.
```
docker login -u <username> -p <access token> https://hydrogen.cloud.nds.rub.de/nexus

docker pull hydrogen.cloud.nds.rub.de/tls-attacker/docker-library/boringssl-server:2623

docker logout
```

We refer to the official [Docker repository documentation](https://docs.docker.com/docker-hub/repos/) for further details on the usage of the docker repository.

# Server Architecture / Nginx

Both the Jenkins server and the Nexus server run behind an Nginx reverse proxy on `hydrogen.cloud.nds.rub.de`. This server also has to have any Maven or Java versions installed which are used in the build pipeline of the Jenkins server. The server allows ssh connections from admitted users.

## Nginx Configuration

The Nginx configuration is located at `etc/nginx/sites-enabled/hydrogen.cloud.nds.rub.de` and ensures that Jenkins and Nexus are only accessible via HTTPS on `/` and `/nexus/` respectively. To add a new service, install it on the virtual machine and add a new `location` in the Nginx configuration file. Remark: In order for Nexus to be accessible at `/nexus/`, we have to set `nexus-context-path=/nexus/` in `opt/nexus/sonatype-work/nexus3/etc/nexus.properties`.

## Maven Configuration

Maven is installed under `etc/maven/`. Here you can also find the `settings.xml` in which you can specify any settings Jenkin should use in its Maven builds. In it, we also instruct Maven to connect to the Nexus Snapshot Repository via the NDS-Jenkins GitHub user

# Deploying to Nexus And Maven Central

For most projects, the latest development version is build by Jenkins and uploaded to the [Nexus Repository](#snapshot-repository--nexus) automatically. To this end, the Jenkins build pipeline compiles all commits to the master / main branches of the "development" repositories and uploads them as snapshots to the Nexus Repository.

To release a stable version (i.e., without the -SNAPSHOT modifier) to Nexus and / or Maven Central one can use the Maven Release Plugin. The plugin is included as part of the Bill of Materials (BOM) and can therefore be used by any project importing or extending upon the BOM. The release consists out of two steps (covered by the commands below):

1. Prepare the release by creating the required commits, tagging the release commit with the version number and pushing the changes to GitHub.
2. Release the tagged release created before to Nexus / Maven Central.

To create a new release issue the following commands:

1. `git branch release/v{Release}`
    - Needed if the master is write protected. Check whether this has been done before for the repo you are releasing
    - If you create a branch, create a PR after you are done
2. `mvn release:prepare`
    - asks which version to prepare and what the next version will be
    - creates commits
    - creates git tag
    - pushes commit+git tag
3. `mvn release:perform`
    - pushes to our nexus
4. `git checkout tags/v{Release}`
    - so that you release the correct version to maven central
5. `mvn deploy -P central`
    - pushes to maven central
    - You can see the progress at [nexus repository manager (StatgingRepositories)](https://s01.oss.sonatype.org/#stagingRepositories)
    - You can pass the passphrase for your GPG key using `-Dgpg.passphrase="PWD"`
        - Keep in mind that this might get logged to your shell history, i.e. the passphrase is then stored in plaintext on your disk
        - If you omit this, it should ask interactively for the passphrase
    - `-DstagingProgressTimeoutMinutes=10`
        - If the push timeouts you can try to increase the timeout a bit
        - However, it seems that it is usually the fault of the server and you should check for an open issue or create one

(Again the commands in a single code block for easy copy+paste)
```bash
git branch release/v{Release}
mvn release:prepare
mvn release:perform

git checkout tags/v{Release}
mvn deploy -P central
```

If the project uses Spotless with the `<ratchetFrom>` configuration, one needs to skip Spotless execution during `mvn release:perform` to avoid missing refspecs. This can be done by appending `-Darguments="-Dspotless.apply.skip"`.

## Prerequisites for Nexus

To be able to push to our [Nexus Repository](#snapshot-repository--nexus) you need a published pgp key.
I am not sure which E-Mail has to be included in the pgp key; probably one of your GitHub email addresses.
Further, you need to be part of the [tls-attacker-extended](https://github.com/orgs/tls-attacker/teams/tls-attacker-extended/members) github group.

## Setting up Maven Central

To deploy to maven central you need to do the following things:

1. Register at the [issue tracker](https://issues.sonatype.org/) of maven central
2. Ask for permissions for [TLS Attacker](https://issues.sonatype.org/browse/OSSRH-61488); Someone who already has developer access must back that request, or they can request it for you. Just look at the history of the linked issue.
    - This may take a day or two
3. Setup credentials for maven
    - Once you have permission you should be able to login to the [Central Portal](https://central.sonatype.com) with the same credentials as you have at the issue tracker
    - On the top right click on your name, "Profile"
    - In the "Profile" pane you have a dropdown that states "Summary"; change that to "User Token"
    - Create a new token by clicking "Access User Token"
    - Copy that token into your `.m2/settings.xml` into the `settings/servers` (cf. [Setting up the Nexus connection](#Setup))
    - Change the id of the just pasted server to `central-upload`.
    - It should look something like this:
      ```xml
      <server>
          <id>central-upload</id>
          <username>random letters</username>
          <password>more random letters</password>
      </server>
      ```
4. Create and Publish a pgp key.
    - The key must be uploaded to a GPG key repository accepted by Sonatype (see [Sonatype Manual](https://central.sonatype.org/publish/requirements/gpg/#distributing-your-public-key)). I used thunderbird for publishing it.
    - I am not sure which E-Mail has to be included in the pgp key; probably the one you used to register at the issue tracker.

You should now be able to run the commands to publish a new release.

# FAQ

## I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development

For the changes to take effect you have to manually install both X.509-Attacker and the TLS-Attacker sub-project. The Snapshot repository only contains the compiled master branches of the development sub-projects.

## I am getting XSD validation errors during a WorkflowTrace copy operation

It is likely that your resource files are out of date. Try running `mvn test` to update your XSD and config files.

## Is there a demo server that I can attack?

The TLS-Attacker sub-project provides an `openssl` server you can run on localhost. If `openssl` is not installed(it should be) you can install it with

```bash
$ apt install openssl
```
You can then start a server that will be accessible at `localhost:4433` using

```bash
$ cd TLS-Attacker/resources
$ ./keygen.sh
$ openssl s_server -key rsa1024key.pem -cert rsa1024cert.pem
```

## I need to build a project frequently but executing the tests takes very long
By default, all unit and integration tests are run upon building a project using mvn install. If you want to skip the more extensive integration tests while still executing basic unit tests, you can use the command below.
```bash
$ mvn clean package && mvn clean install -DskipTests
```

## I did not find my problem or question. Where can I ask for help?

This documentation is still under construction. We would greatly appreciate constructive feedback in the issues of this repository. You can also add a section or question to the FAQ via a pull request. You can ask also ask questions in the issues of the respective GitHub repository.
