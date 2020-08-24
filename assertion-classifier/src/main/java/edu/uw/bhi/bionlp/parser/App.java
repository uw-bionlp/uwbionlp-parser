package edu.uw.bhi.bionlp.parser;

import io.grpc.*;

public class App 
{
    public static void main( String[] args ) throws Exception
    {
      Server server = ServerBuilder.forPort(8080)
        .addService(new AssertionClassifierImpl())
        .build();

      // Start the server
      server.start();

      // Don't exit the main thread. Wait until server is terminated.
      server.awaitTermination();
    }
}

// mvn -DskipTests package exec:java -Dexec.mainClass=edu.uw.bhi.bionlp.parser.App

// docker build -t uwbionlp-assert -f assertion-classifier/Dockerfile assertion-classifier
// docker run -d --name uwbionlp-assert -p 8080:8080 uwbionlp-assert