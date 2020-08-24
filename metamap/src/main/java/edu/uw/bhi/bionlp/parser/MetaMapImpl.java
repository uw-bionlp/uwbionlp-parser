package edu.uw.bhi.bionlp.parser;

import java.util.List;

import org.javatuples.Pair;

import edu.uw.bhi.bionlp.parser.Uwbionlp.MetaMapInput;
import edu.uw.bhi.bionlp.parser.Uwbionlp.MetaMapOutput;
import edu.uw.bhi.bionlp.parser.Uwbionlp.MetaMapSentence;
import edu.uw.bhi.bionlp.parser.MetaMapGrpc.MetaMapImplBase;
import io.grpc.stub.StreamObserver;

/**
 *
 * @author ndobb
 */
public class MetaMapImpl extends MetaMapImplBase {

    DocumentProcessor processor;

    public MetaMapImpl() {
        this.processor = new DocumentProcessor();
    }

    @Override
    public void extractNamedEntities(MetaMapInput request, StreamObserver<MetaMapOutput> responseObserver) {

        /*
         * Process. Output is a tuple<sentences,errors>.
         */
        Pair<List<MetaMapSentence>, List<String>> output = processor.processDocument(
            request.getSentencesList(), 
            request.getSemanticTypesList()
        );
        
        MetaMapOutput response = MetaMapOutput.newBuilder()
            .addAllSentences(output.getValue0())
            .addAllErrors(output.getValue1())
            .setId(request.getId())
            .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}