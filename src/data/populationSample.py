from scipy.stats import binom 
import frequencyDictionary as fd

class PopulationSample:
    def __init__():
        pass


    # create population sample - see idea.txt
    def create(self):
        dict, totalCount = fd.FrequencyDictionary().get()
        
        # estimate probabilities p1..pN 
        dictProb = self.estimateProbsOfWordOccurence(dict, totalCount)

           
    def estimateProbsOfWordOccurence(self, dict, totalCount):
        dictProb = {}
        for key in dict:
            dictProb[key] = dict[key]/totalCount
        return dictProb


    def estimateProbsOfWordKnowledge(sampleSize, requieredOccurence, word, dictProb):
        p = dictProb[word]
        n = sampleSize
        k = requieredOccurence
        r_values = list(range(k-1)) 
        return 1-sum([binom.pmf(r, n, p) for r in r_values])


