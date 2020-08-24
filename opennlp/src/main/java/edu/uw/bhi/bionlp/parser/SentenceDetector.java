package edu.uw.bhi.bionlp.parser;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.util.Span;

/**
 *
 * @author ndobb
 */
public class SentenceDetector {

    SentenceDetectorME sentenceDetector;

    public SentenceDetector() {

        try {
            InputStream modelIn = new FileInputStream("resources/open-nlp/en-sent.bin");
            SentenceModel model = new SentenceModel(modelIn);
            sentenceDetector = new SentenceDetectorME(model);
        } catch (Exception ex) {
            System.out.println(ex.getStackTrace());
            System.out.println(ex.getMessage());
        }
    }

    public List<Span> detectBoundaries(String text) {
        return Arrays.asList(sentenceDetector.sentPosDetect(text));
    }

    public List<String> getSentences(String text) {
        return Arrays.asList(sentenceDetector.sentDetect(text));
    }
}