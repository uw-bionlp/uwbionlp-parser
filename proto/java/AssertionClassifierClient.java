package edu.uw.bhi.bionlp.covid.parser.grpcclient;

import edu.uw.bhi.bionlp.covid.parser.AssertionClassifierGrpc;
import edu.uw.bhi.bionlp.covid.parser.AssertionClassifierGrpc.*;
import edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierInput;
import edu.uw.bhi.bionlp.covid.parser.CovidParser.AssertionClassifierOutput;
import io.grpc.Channel;
import io.grpc.ManagedChannelBuilder;

public class AssertionClassifierClient {

    private final AssertionClassifierBlockingStub blockingStub;

    public AssertionClassifierClient() {

        Channel channel = ManagedChannelBuilder.forAddress("assertion-classifier", 8080).usePlaintext(true).build();
        blockingStub = AssertionClassifierGrpc.newBlockingStub(channel);
    }

    public String predictAssertion(String sentence, int beginIndex, int endIndex) {

        AssertionClassifierOutput output;
        AssertionClassifierInput request = AssertionClassifierInput.newBuilder()
            .setText(sentence)
            .setStartCharIndex(beginIndex)
            .setEndCharIndex(endIndex)
            .build();

        try {
            output = blockingStub.predictAssertion(request);
        } catch (Exception ex) {
            return "present";
        }
        return output.getPrediction();
    }
}