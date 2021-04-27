/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.rub.nds.tls.attacker.template;

import de.rub.nds.tlsattacker.core.config.Config;
import de.rub.nds.tlsattacker.core.constants.CipherSuite;
import de.rub.nds.tlsattacker.core.constants.HandshakeMessageType;
import de.rub.nds.tlsattacker.core.constants.ProtocolVersion;
import de.rub.nds.tlsattacker.core.constants.RunningModeType;
import de.rub.nds.tlsattacker.core.protocol.message.ChangeCipherSpecMessage;
import de.rub.nds.tlsattacker.core.protocol.message.ClientHelloMessage;
import de.rub.nds.tlsattacker.core.protocol.message.FinishedMessage;
import de.rub.nds.tlsattacker.core.protocol.message.RSAClientKeyExchangeMessage;
import de.rub.nds.tlsattacker.core.protocol.message.ServerHelloMessage;
import de.rub.nds.tlsattacker.core.state.State;
import de.rub.nds.tlsattacker.core.workflow.DefaultWorkflowExecutor;
import de.rub.nds.tlsattacker.core.workflow.WorkflowExecutor;
import de.rub.nds.tlsattacker.core.workflow.WorkflowTrace;
import de.rub.nds.tlsattacker.core.workflow.WorkflowTraceUtil;
import de.rub.nds.tlsattacker.core.workflow.action.GenericReceiveAction;
import de.rub.nds.tlsattacker.core.workflow.action.SendAction;
import de.rub.nds.tlsattacker.core.workflow.action.WaitAction;
import java.security.Security;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

public class ExampleClass {

    public static void main(String args[]) {
        //Make sure to add BouncyCastle as a security provider
        Security.addProvider(new BouncyCastleProvider());
        //This is an example TLS-Attacker application
        //Lets do some basic stuff
        //we create some basic config with default values
        Config config = Config.createConfig();
        //we specify where we want to connect to
        //you can change the runningmode to server and adjust the defaultServerConnection if you 
        //want to run TLS-Attacker as a server
        config.setDefaultRunningMode(RunningModeType.CLIENT);
        config.getDefaultClientConnection().setHostname(args[0]);
        config.getDefaultClientConnection().setPort(Integer.parseInt(args[1]));
        config.getDefaultClientConnection().setTimeout(200);
        //We add some extensions
        config.setAddClientAuthzExtension(Boolean.TRUE);
        config.setAddHeartbeatExtension(Boolean.TRUE);
        //We specify some more parameters
        config.setDefaultClientSupportedCiphersuites(CipherSuite.TLS_RSA_WITH_AES_128_CBC_SHA, CipherSuite.TLS_RSA_WITH_AES_256_CBC_SHA);        
        config.setHighestProtocolVersion(ProtocolVersion.fromString(args[2]));
        //Now lets specify a WorkflowTrace
        WorkflowTrace trace = new WorkflowTrace();
        //Send a ClientHello with the specified extensions
        trace.addTlsAction(new SendAction(new ClientHelloMessage(config)));
        //Receive Some messages (we dont know how the server will react
        trace.addTlsAction(new GenericReceiveAction());
        //Now lets wait 2 seconds (why not :) )
        trace.addTlsAction(new WaitAction(2000));
        //Now lets send an rsa client key exchange message + ccs + finished
        trace.addTlsAction(new SendAction(new RSAClientKeyExchangeMessage(config), new ChangeCipherSpecMessage(config), new FinishedMessage(config)));
        //Lets see what the other party has to say about this
        trace.addTlsAction(new GenericReceiveAction());
        //now lets send a ServerHello message after the Handshake was executed
        trace.addTlsAction(new SendAction(new ServerHelloMessage(config)));
        //lets see what the other party has to say about this
        trace.addTlsAction(new GenericReceiveAction());

        //Lets execute the Trace
        State state = new State(config, trace);
        WorkflowExecutor executor = new DefaultWorkflowExecutor(state);
        executor.executeWorkflow();
        //Ok the trace was now executed. Lets analyze it
        System.out.println("Received Finished:" + WorkflowTraceUtil.didReceiveMessage(HandshakeMessageType.FINISHED, trace));
        System.out.println("Selected CipherSuite: " + state.getTlsContext().getSelectedCipherSuite());
    }
}
