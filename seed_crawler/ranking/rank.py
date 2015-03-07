import sys

import tfidf
import BayesianSets
import numpy as np

class rank:
    def results(self,input_file,query_index,ignore_index):
        table = tfidf.tfidf()
    
        # Compute tfidf of terms in the documents
        adjusted_indices = table.process(input_file, ignore_index)
        query_index_copy = query_index
        
        query_index = [adjusted_indices[x] for x in query_index_copy]
        
        data = table.getTfidfArray()

        bs = BayesianSets.BayesianSets()
    
        # documents other than the relevant documents
        index = [x for x in range(0,len(data)) if x not in query_index ]

        score = bs.score(data[query_index,:], data[index,:])

        rank_index = np.argsort(np.multiply(score,-1))

        offset_rank_index = [index[x] for x in rank_index]

        # Get the urls corresponding to the scored documents
        ranked_urls = table.getURLs(offset_rank_index)

        ranked_scores = [score[rank_index[i]] for i in range(0, len(score))]
        return [ranked_urls,ranked_scores]

def main(argv):
    if len(argv) != 2:
        print "Invalid arguments"
        print "python rank.py inputfile 0,1,2"
        return
    
    # File containing information of documents
    input_file = argv[0]
    # Most relevant documents
    query_index = [int(i) for i in argv[1].split(',')]
    ranker = rank()
    [ranked_urls,scores] = ranker.results(input_file,query_index)

    for i in range(0,len(ranked_urls)):
        print ranked_urls[i]," ", str(scores[i])
    
if __name__=="__main__":
    main(sys.argv[1:])
