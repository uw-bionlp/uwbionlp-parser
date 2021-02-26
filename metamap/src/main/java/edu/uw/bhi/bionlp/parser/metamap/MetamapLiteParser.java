package edu.uw.bhi.bionlp.parser.metamap;

import bioc.BioCSentence;
import edu.uw.bhi.bionlp.parser.data.MetaMapParseResult;
import edu.uw.bhi.bionlp.parser.data.UMLSConcept;
import gov.nih.nlm.nls.metamap.lite.types.ConceptInfo;
import gov.nih.nlm.nls.metamap.lite.types.Entity;
import gov.nih.nlm.nls.metamap.lite.types.EntityTokenList;
import gov.nih.nlm.nls.metamap.lite.types.Ev;
import gov.nih.nlm.nls.metamap.prefix.ERToken;
import gov.nih.nlm.nls.ner.MetaMapLite;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author ndobb
 */
public class MetamapLiteParser implements IMetamapParser {

    Properties myProperties;
    MetaMapLite metaMapLiteInst;

    public MetamapLiteParser() {
        try {
            myProperties = new Properties();
            MetaMapLite.expandModelsDir(myProperties, "resources/public_mm_lite/data/models");
            MetaMapLite.expandIndexDir(myProperties, "resources/public_mm_lite/data/ivf/2020AA/USAbase");
            myProperties.setProperty("metamaplite.excluded.termsfile", "resources/public_mm_lite/data/specialterms.txt");
            myProperties.setProperty("metamaplite.enable.postagging", "false");
            myProperties.setProperty("metamaplite.detect.negations", "false");
            myProperties.setProperty("metamaplite.enable.scoring", "false");
            myProperties.setProperty("metamaplite.index.directory", "resources/public_mm_lite/data/ivf/2020AA/USAbase");
            metaMapLiteInst = new MetaMapLite(myProperties);

        } catch (Exception ex) {
            Logger.getLogger(MetamapLiteParser.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println(ex.getMessage());
            System.out.println(ex.getStackTrace());
        }
    }

    public MetaMapParseResult parseSentenceWithMetamap(String sentenceText, HashSet<String> semanticTypesOfInterest) throws Exception {
        List<UMLSConcept> concepts = new ArrayList<UMLSConcept>();
        BioCSentence sentence = new BioCSentence();
        sentence.setText(sentenceText);
        sentence.setOffset(0);

        EntityTokenList entityList = metaMapLiteInst.processSimpleSentence(sentence);
        String[] tokens = getTokensFromMetamapParse(entityList.getTokens());

        for (Entity entity : entityList.getEntities()) {
            String matchedText = entity.getMatchedText();
            int charStartIdx = entity.getStart();
            int charStopIdx = charStartIdx + entity.getLength();
            int tokStartIdx = entity.getBeginTokenIndex();
            int tokStopIdx = entity.getBeginTokenIndex();
            HashSet<String> cuiList = new HashSet<String>();

            for (Ev ev : entity.getEvSet()) {
                ConceptInfo conceptInfo = ev.getConceptInfo();
                String cui = conceptInfo.getCUI();
                Set<String> semanticTypes = conceptInfo.getSemanticTypeSet();
                
                if (Collections.disjoint(semanticTypesOfInterest, semanticTypes)) {
                    continue;
                }

                if (!cuiList.contains(cui)) {
                    UMLSConcept concept = new UMLSConcept();
                    concept.setCUI(cui);
                    concept.setConceptName(conceptInfo.getPreferredName());
                    concept.setPhrase(matchedText);
                    concept.setBeginCharIndex(charStartIdx);
                    concept.setEndCharIndex(charStopIdx);
                    concept.setBeginTokenIndex(tokStartIdx);
                    concept.setEndTokenIndex(tokStopIdx);
                    concept.setSemanticTypeLabels(semanticTypes);
                    concepts.add(concept);
                    cuiList.add(cui);
                }
            }
        }
        return new MetaMapParseResult(concepts, tokens);
    }

    String[] getTokensFromMetamapParse(List<ERToken> mmTokens) {
        List<String> tokens = new ArrayList<String>();
        int prevIdx = -1;

        for (ERToken tok : mmTokens) {
            int idx = tok.getIndex();
            if (idx != prevIdx) {
                tokens.add((tok.getText()));
            }
            prevIdx = idx;
        }
        String[] arrTokens = new String[tokens.size()];
        for (int i = 0; i < tokens.size(); i++) {
            arrTokens[i] = tokens.get(i);
        }
        return arrTokens;
    }
}