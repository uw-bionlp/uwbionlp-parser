package edu.uw.bhi.bionlp.parser;

import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.tokenize.TokenizerME;

import java.io.FileInputStream;
import java.io.InputStream;

/**
 *
 * @author ndobb
 */
public class Tokenizer {
    private TokenizerModel model;
    private TokenizerME tokenizer;

    public Tokenizer() {
        try {
            InputStream modelIn = new FileInputStream("resources/public_mm_lite/data/models/en-token.bin");
            this.model = new TokenizerModel(modelIn);
            this.tokenizer = new TokenizerME(model);
        } catch (Exception ex) {
            System.out.println(ex.toString());
        }
    }

    public String[] tokenize(String sentence) {
        return tokenizer.tokenize(sentence);
    }
}