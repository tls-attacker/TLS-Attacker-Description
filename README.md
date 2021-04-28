# TLS-Attacker-Description

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

If you want to install a runnable jar (for example the TLS-Scanner sub-project to scan your server) you can install it manually from Github. An example for the TLS-Scanner would be

```bash
$ git clone https://github.com/tls-attacker/TLS-Scanner.git
$ cd TLS-Scanner
$ mvn clean install
```
All internal dependencies are resolved by Maven using the Maven central repository.

The jar files are accessible in the "apps" folder. If you want to copy the jar files remember to copy the "apps/lib" folder as well, it contains the dependencies of the final jar.

## Development Versions/Snapshots

The compiled "Snapshot" jars from the development repositories are not uploaded to Maven Central. You either have to download all sub-projects from Github and install them manually or you can download them from the Nexus Snapshot repository. 

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

The [Jenkins build pipeline](#the-build-pipeline--jenkins) will test and compile your pull request and checks whether [license headers](#license-headers) and the [visual formatting](#code-style) is up to date. If any of the checks fail Jenkins will tell you on your pull request. Any fixes or changes you commit to your branch will be included in your pull request and checked again by Jenkins.

Before your change or fix can be merged into the master branch, a maintainer has to approve your pull request. Before they do so, they might give you feedback in the form of comments on your pull requests. After you resolved the feedback (or asked questions on the feedback) a maintainer will review your pull request again. This process is repeated until the pull request is finally merged.

If you want a specific maintainer to review your pull request (maybe your thesis advisor), you can request one on Github. You can also mention other users in your pull request if you believe they can help with something or would be interested in your change/fix.

We know it can take some time until your pull request might be merged, but please be patient :)

# The build pipeline / Jenkins



# Snapshot Repository / Nexus

# Deploying to Nexus And Maven Central

# FAQ

## I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development

For the changes to take effect you have to manually install both X.509-Attacker and the TLS-Attacker sub-project. The Snapshot repository only contains the compiled master branches of the development sub-projects.

## I am getting XSD validation errors during a WorkflowTrace copy operation

It is likely that your resource files are out of date. Try running `mvn test` to update your XSD and config files.