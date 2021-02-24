package edu.uw.bhi.bionlp.parser;

import io.grpc.*;

public class App 
{
    public static void main( String[] args ) throws Exception
    {
      // Build server
      Server server = ServerBuilder.forPort(8080)
        .addService(new MetaMapImpl())
        .build();

      // Start the server
      server.start();

      // Don't exit the main thread. Wait until server is terminated.
      server.awaitTermination();
    }
}

// mvn dependency:purge-local-repository
// mvn -DskipTests package exec:java -Dexec.mainClass=edu.uw.bhi.bionlp.parser.App

// docker build -t uwbionlp-metamap -f metamap/Dockerfile metamap
// docker run -d --name uwbionlp-metamap -p 8080:8080 uwbionlp-metamap