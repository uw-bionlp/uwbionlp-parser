package edu.uw.bhi.bionlp.parser.metamap;

import edu.uw.bhi.bionlp.parser.data.MetaMapParseResult;

import java.util.HashSet;

/**
 *
 * @author wlau
 * @author ndobb
 */
public interface IMetamapParser {

    MetaMapParseResult parseSentenceWithMetamap(String sentenceText, HashSet<String> semanticTypesOfInterest) throws Exception;
}