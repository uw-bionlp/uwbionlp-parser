package edu.uw.bhi.bionlp.parser.data;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * Author: melihay Date: Jun 28, 2012 Time: 11:31:09 AM Version: 1.0
 */
public class UMLSConcept {
    private String CUI;
    private String conceptName;
    private String phrase; // phrase the concept identified in
    private List<String> semanticTypeLabels;
    private int beginTokenIndex;
    private int endTokenIndex;
    private int beginCharIndex;
    private int endCharIndex;

    public String toString() {
        String str = "";
        str += this.getCUI()+"\t"+"PHRASE:"+this.getPhrase()+"\tSTR:"+this.getConceptName()+"\tSEMTYPES:"+this.getSemanticTypeLabels();
        return str;
    }

    public String getCUI() {
        return CUI;
    }

    public void setCUI(String CUI) {
        this.CUI = CUI;
    }

    public String getPhrase() {
        return phrase;
    }

    public void setPhrase(String phrase) {
        this.phrase = phrase;
    }

    public String getConceptName() {
        return conceptName;
    }

    public void setConceptName(String conceptName) {
        this.conceptName = conceptName;
    }

    public int getBeginTokenIndex() {
        return beginTokenIndex;
    }

    public void setBeginTokenIndex(int beginTokenIndex) {
        this.beginTokenIndex = beginTokenIndex;
    }

    public int getEndTokenIndex() {
        return endTokenIndex;
    }

    public void setEndTokenIndex(int endTokenIndex) {
        this.endTokenIndex = endTokenIndex;
    }

    public int getBeginCharIndex() {
        return beginCharIndex;
    }

    public void setBeginCharIndex(int beginCharIndex) {
        this.beginCharIndex = beginCharIndex;
    }

    public int getEndCharIndex() {
        return endCharIndex;
    }

    public void setEndCharIndex(int endCharIndex) {
        this.endCharIndex = endCharIndex;
    }

    public List<String> getSemanticTypeLabels() {
        return semanticTypeLabels;
    }

    public void setSemanticTypeLabels(List<String> semanticTypeLabels) {
        this.semanticTypeLabels = semanticTypeLabels;
    }

    public void setSemanticTypeLabels(Set<String> semanticTypeLabels) {
        this.semanticTypeLabels = new ArrayList<String>(semanticTypeLabels);
    }
}