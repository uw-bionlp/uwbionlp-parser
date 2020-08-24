package edu.uw.bhi.bionlp.parser;

import java.util.List;
import java.io.File;
import java.nio.file.Files;
import java.text.Normalizer;
import java.text.Normalizer.Form;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;

import org.javatuples.Pair;

import edu.uw.bhi.bionlp.parser.Uwbionlp.MetaMapConcept;
import edu.uw.bhi.bionlp.parser.Uwbionlp.MetaMapSentence;
import edu.uw.bhi.bionlp.parser.Uwbionlp.Sentence;
import edu.uw.bhi.bionlp.parser.data.UMLSConcept;
import edu.uw.bhi.bionlp.parser.metamap.MetamapLiteParser;


public class DocumentProcessor {

    AssertionClassifier assertionClassifier = new AssertionClassifier();
    MetamapLiteParser parser = new MetamapLiteParser();
    MetaMapConcept.Builder conceptBuilder = MetaMapConcept.newBuilder();
    HashSet<String> allSemanticTypes = loadSemanticTypes();

    public Pair<List<MetaMapSentence>, List<String>> processDocument(List<Sentence> sentences, List<String> semanticTypesOfInterest) {
        /**
         * Initialize lists.
         */
        List<MetaMapSentence> mmSentences = new ArrayList<MetaMapSentence>();
        List<String> errors = new ArrayList<String>();
        
        HashSet<String> semanticTypes = semanticTypesOfInterest == null || semanticTypesOfInterest.size() == 0
            ? allSemanticTypes
            : collToHashSet(semanticTypesOfInterest);

        /*
         * For each sentence.
         */
        for (int sId = 0; sId < sentences.size(); sId++) {
            List<MetaMapConcept> mmCons = new ArrayList<MetaMapConcept>();
            Sentence sentence = sentences.get(sId);
            String normalized = Normalizer.normalize(sentence.getText(), Form.NFKC).trim().replaceAll(" +", " ");
            HashMap<String,String> assertionCache = new HashMap<String,String>();

            /* 
             * Extract UMLS concepts.
             */
            List<UMLSConcept> concepts = new ArrayList<UMLSConcept>();
            try {
                concepts = parser.parseSentenceWithMetamap(normalized, semanticTypes);
            } catch (Exception ex) {
                String errorMsg = "Error: failed to parse with Metamap. Sentence" + sId + ": '" + normalized + "'. Error: " + ex.getMessage();
                errors.add(errorMsg);
            }

            /*
             * For each concept.
             */
            for (UMLSConcept concept : concepts) {
                String prediction = "present";
                try {
                    
                    /*
                     * Check if this span has been seen before, if so use cached 
                     * rather than re-checking assertion.
                     */ 
                    String inputs = concept.getBeginCharIndex() + "|" + concept.getEndCharIndex();
                    if (assertionCache.containsKey(inputs)) {
                        prediction = assertionCache.get(inputs);

                    /*
                     * Else predict assertion.
                     */
                    } else {
                        Pair<String,String> predicted = assertionClassifier.predict(normalized, concept.getBeginCharIndex(), concept.getEndCharIndex());
                        prediction = predicted.getValue0();

                        if (predicted.getValue1() != null) {
                            errors.add(predicted.getValue1());
                        } else {
                            assertionCache.put(inputs, prediction);
                        }
                    }
                } catch (Exception ex) {
                    // do nothing, error caught above

                /*
                 * Add the final concept.
                 */
                } finally {
                    MetaMapConcept mmCon = conceptBuilder
                        .setConceptName(concept.getConceptName())
                        .setCui(concept.getCUI())
                        .setBeginSentCharIndex(concept.getBeginCharIndex())
                        .setEndSentCharIndex(concept.getEndCharIndex())
                        .setBeginDocCharIndex(sentence.getBeginCharIndex() + concept.getBeginCharIndex())
                        .setEndDocCharIndex(sentence.getBeginCharIndex() + concept.getEndCharIndex())
                        .setSourcePhrase(concept.getPhrase())
                        .setPrediction(prediction)
                        .clearSemanticTypes()
                        .addAllSemanticTypes(concept.getSemanticTypeLabels())
                        .build();
                        mmCons.add(mmCon);
                }
            }
            MetaMapSentence mmSent = MetaMapSentence
                .newBuilder()
                .setBeginCharIndex(sentence.getBeginCharIndex())
                .setEndCharIndex(sentence.getEndCharIndex())
                .addAllConcepts(mmCons)
                .setId(sentence.getId())
                .setText(sentence.getText())
                .build();
            mmSentences.add(mmSent);
        }
        return new Pair<List<MetaMapSentence>, List<String>>(mmSentences, errors);
    }

    HashSet<String> loadSemanticTypes() {
        HashSet<String> set = new HashSet<String>();
        try {
            String file = new String(Files.readAllBytes(new File("resources/umls/umls_semantic_type_labels.txt").toPath()));
            set = collToHashSet(Arrays.asList(file.split("\n")));
        } catch (Exception ex) {
            // Do nothing for now.
        }
        return set;
    }

    HashSet<String> collToHashSet(Collection<String> values) {
        HashSet<String> set = new HashSet<String>();
        for (String value : values) {
            set.add(value.trim());
        }
        return set;
    }
}