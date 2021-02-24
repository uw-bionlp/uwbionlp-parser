package edu.uw.bhi.bionlp.parser;

import edu.uw.bhi.uwassert.AssertionClassifier;

import org.javatuples.Pair;

/**
 *
 * @author ndobb
 */
public class AssertionClassification {
    private AssertionClassifier assertionClassifier = new AssertionClassifier();

    static {
        System.setProperty("CONFIGFILE", "resources/assertion-classifier/assertcls.properties");
        System.setProperty("ASSERTRESOURCES", "resources/assertion-classifier");
    }

    Pair<String,String> predict (String[] tokens, int startIndex, int endIndex) {
        String prediction = "indeterminate";
        
        try {
            prediction = assertionClassifier.predict(tokens, startIndex, endIndex);  
            return new Pair<String,String>(prediction, null);
        } catch (Exception ex) {
            return new Pair<String,String>(prediction, ex.toString());
        }
    }

    Pair<String,String> predict (String sentence, int startCharIndex, int endCharIndex) {
        String prediction = "indeterminate";
        String ngram = "";
        int size = 10;
        
        try {
            NgramParameters params = getNgram(sentence, size, startCharIndex, endCharIndex);
            ngram = params.ngram;
            prediction = assertionClassifier.predict(ngram, params.beginTokenIndex, params.endTokenIndex);  
            return new Pair<String,String>(prediction, null);
        } catch (Exception ex) {
            String err = "Error: failed to assert. NGram: '" + ngram + "', StartIndex: " + startCharIndex + ", EndIndex: " + endCharIndex + ". Error: '" + ex.getMessage() + "'";
            return new Pair<String,String>(prediction, err);
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