package edu.uw.bhi.bionlp.parser;

import edu.uw.bhi.bionlp.parser.AssertionClassifierGrpc.AssertionClassifierImplBase;
import edu.uw.bhi.bionlp.parser.Uwbionlp.AssertionClassifierInput;
import edu.uw.bhi.bionlp.parser.Uwbionlp.AssertionClassifierOutput;
import edu.uw.bhi.uwassert.AssertionClassification;
import io.grpc.stub.StreamObserver;

import name.adibejan.util.IntPair;

/**
 *
 * @author ndobb
 */
public class AssertionClassifierImpl extends AssertionClassifierImplBase {
    static {
        System.setProperty("CONFIGFILE",
                    "resources/assertion-classifier/assertcls.properties");
        System.setProperty("ASSERTRESOURCES",
                    "resources/assertion-classifier");
        System.setProperty("LIBLINEAR_PATH",
                    "resources/assertion-classifier/liblinear-1.93");
    }

    @Override
    public void predictAssertion(AssertionClassifierInput input, StreamObserver<AssertionClassifierOutput> responseObserver) {

        String prediction = predict(input.getText(), input.getStartCharIndex(), input.getEndCharIndex());
        AssertionClassifierOutput response = AssertionClassifierOutput
            .newBuilder()
            .setPrediction(prediction)
            .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    String predict (String sentence, int startIndex, int endIndex) {
        try {
            NgramParameters params = getNgram(sentence, 10, startIndex, endIndex);
            return AssertionClassification.predict(params.ngram, new IntPair(params.beginTokenIndex, params.endTokenIndex));  
        } catch (Exception ex) {
            System.out.println("Error: failed to assert. Sentence: '" + sentence + "', StartIndex: " + startIndex + ", EndIndex: " + endIndex + ". " + ex.getMessage());
            return "present";
        }
    }

    NgramParameters getNgram(String sentence, int ngramSize, int beginCharIndex, int endCharIndex) {
        int lastChar = sentence.length()-1;
        int precCnt = 0;
        int follCnt = 0;
        int startPos = beginCharIndex;
        int endPos = endCharIndex;
        boolean isSpace = false;
        boolean prevWasSpace = true;
        String sent = sentence.replaceAll("\n", " ");

        // Get preceding
        while (startPos > -1) {
            isSpace = sent.charAt(startPos) == ' ';
            if (isSpace && !prevWasSpace) {
                precCnt++;
            }
            if (startPos == 0 || precCnt > ngramSize) {
                if (precCnt > ngramSize) {
                    precCnt = ngramSize;
                }
                break;
            }
            startPos--;
            prevWasSpace = isSpace;
        }

        // Get following
        prevWasSpace = true;
        while (endPos <= lastChar) {
            isSpace = sent.charAt(endPos) == ' ';
            if (isSpace && !prevWasSpace) {
                follCnt++;
            }
            if (endPos == lastChar || follCnt == ngramSize) {
                break;
            }
            endPos++;
            prevWasSpace = isSpace;
        }

        return new NgramParameters(
            sent.substring(startPos, endPos).trim(), 
            precCnt, 
            precCnt + sent.substring(beginCharIndex, endCharIndex).split(" ").length-1
        );
    }
}

class NgramParameters {
    public String ngram;
    public int beginTokenIndex;
    public int endTokenIndex;

    public NgramParameters(String ngram, int beginTokenIndex, int endTokenIndex) {
        this.ngram = ngram;
        this.beginTokenIndex = beginTokenIndex;
        this.endTokenIndex = endTokenIndex;
    }
}