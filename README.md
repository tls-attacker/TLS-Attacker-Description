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



# The build pipeline / Jenkins

# Snapshot Repository / Nexus

# Deploying to Nexus And Maven Central

# FAQ

## I made a change to X.509-Attacker-Development and it does not show up in TLS-Attacker-Development

For the changes to take effect you have to manually install both X.509-Attacker and the TLS-Attacker sub-project. The Snapshot repository only contains the compiled master branches of the development sub-projects.