package edu.uw.bhi.bionlp.parser.data;

import java.util.List;

public class MetaMapParseResult {
    List<UMLSConcept> concepts;
    String[] tokens;

    public MetaMapParseResult(List<UMLSConcept> concepts, String[] tokens) {
        this.concepts = concepts;
        this.tokens = tokens;
    }

    public List<UMLSConcept> getConcepts() {
        return this.concepts;
    }

    public String[] getTokens() {
        return this.tokens;
    }
}
