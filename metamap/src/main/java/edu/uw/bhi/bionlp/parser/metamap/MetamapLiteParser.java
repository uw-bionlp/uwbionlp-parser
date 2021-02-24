package edu.uw.bhi.bionlp.parser.metamap;

import bioc.BioCDocument;
import edu.uw.bhi.bionlp.parser.data.UMLSConcept;
import gov.nih.nlm.nls.metamap.document.FreeText;
import gov.nih.nlm.nls.metamap.lite.types.ConceptInfo;
import gov.nih.nlm.nls.metamap.lite.types.Entity;
import gov.nih.nlm.nls.metamap.lite.types.Ev;
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
            MetaMapLite.expandIndexDir(myProperties, "resources/public_mm_lite/data/ivf");
            myProperties.setProperty("metamaplite.excluded.termsfile", "resources/public_mm_lite/data/specialterms.txt");
            myProperties.setProperty("metamaplite.detect.negations", "false");
            myProperties.setProperty("metamaplite.index.directory", "resources/public_mm_lite/data/ivf");
            metaMapLiteInst = new MetaMapLite(myProperties);

        } catch (Exception ex) {
            Logger.getLogger(MetamapLiteParser.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println(ex.getMessage());
            System.out.println(ex.getStackTrace());
        }
    }

    public List<Entity> parseSentenceWithMetamap(BioCDocument document) throws Exception {
        return metaMapLiteInst.processDocument(document);
    }

    public List<UMLSConcept> parseSentenceWithMetamap(String sentenceText, HashSet<String> semanticTypesOfInterest) throws Exception {
        BioCDocument document = FreeText.instantiateBioCDocument(sentenceText);
        document.setID("1");

        List<UMLSConcept> concepts = new ArrayList<UMLSConcept>();
        List<Entity> resultList = metaMapLiteInst.processDocument(document);

        for (Entity entity : resultList) {
            String matchedText = entity.getMatchedText();
            int charStartIdx = entity.getStart();
            int charStopIdx = charStartIdx + entity.getLength();
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
                    concept.setSemanticTypeLabels(semanticTypes);
                    concepts.add(concept);
                    cuiList.add(cui);
                }
            }
        }
        return concepts;
    }
}