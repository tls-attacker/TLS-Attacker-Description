# TLS-Attacker-Project-Template
This is an example Maven project which uses TLS-Attacker as a library. It provies a basic pom.xml which you can adjust to your needs and some basic code on how to call TLS-Attacker code.
First of all you need to install TLS-Attacker. If you already did that you can skip this step.
```
git clone https://github.com/RUB-NDS/TLS-Attacker.git
cd TLS-Attacker
mvn clean install
cd ..
\\Now you can clone this project 
git clone https://github.com/RUB-NDS/TLS-Attacker-Project-Template.git
cd TLS-Attacker-Project-Template
```
Now you should have everything you need. You can build the example project with:
```
mvn clean package
```
After you built the project you can run the jar from the apps folder.
```
java -jar apps/TLS-Attacker-Template.jar "10.160.160.3" "50001" "TLS12"
```
The example code specifies a basic config with an example WorkflowTrace. It then tries to connect to a server on 10.160.160.3 at port 50001. If there is no Server listening on that port you will get an ConfigurationException.
We internally use Netbeans to work with TLS-Attacker. However you can use the IDE of your choice. If you have questions just contact @ic0nz1, @jurajsomorovsky or create an issue here on github.

Have fun :)
