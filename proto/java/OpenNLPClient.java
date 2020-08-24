package edu.uw.bhi.bionlp.covid.parser.grpcclient;

import java.util.ArrayList;
import java.util.List;

import edu.uw.bhi.bionlp.covid.parser.OpenNLPGrpc;
import edu.uw.bhi.bionlp.covid.parser.CovidParser.Sentence;
import edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionInput;
import edu.uw.bhi.bionlp.covid.parser.CovidParser.SentenceDetectionOutput;
import edu.uw.bhi.bionlp.covid.parser.OpenNLPGrpc.*;
import io.grpc.Channel;
import io.grpc.ManagedChannelBuilder;

public class OpenNLPClient {

    private final OpenNLPBlockingStub blockingStub;

    public OpenNLPClient() {

        Channel channel = ManagedChannelBuilder.forAddress("open-nlp", 8080).usePlaintext(true).build();
        blockingStub = OpenNLPGrpc.newBlockingStub(channel);
    }

    public List<Sentence> detectSentences(String text) {

        SentenceDetectionOutput output;
        SentenceDetectionInput request = SentenceDetectionInput.newBuilder().setText(text).build();

        try {
            output = blockingStub.detectSentences(request);
        } catch (Exception ex) {
            return new ArrayList<Sentence>();
        }
        return output.getSentencesList();
    }
}