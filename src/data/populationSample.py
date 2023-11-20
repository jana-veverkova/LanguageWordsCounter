import scipy.stats as stats
import numpy as np
import csv
import math
from p_tqdm import p_map, p_umap, p_imap, p_uimap
from tqdm import tqdm
import src.data.frequencyDictionary as fd

class PopulationSample:
    def __init__(self):
        pass


    # create population sample - see idea.txt
    def create(self):
        frequencyDict, totalCount = fd.FrequencyDictionary().getByWord()
        
        # estimate probabilities p1..pN 
        self.probabilityDict = self.estimateProbsOfWordOccurence(frequencyDict, totalCount)

        self.requieredOccurence = 15

        n1 = np.arange(1000, 1000000, 1000)
        n2 = np.arange(1000000, 2000000, 1000)
        n3 = np.arange(2000000, 3000000, 1000)
        n4 = np.arange(3000000, 4000000, 1000)
        n5 = np.arange(4000000, 5000000, 1000)
        n6 = np.arange(5000000, 6000000, 1000)
        n7 = np.arange(5000000, 8000000, 3000)

        results = p_map(self.generatePersonSample, n7)

        with open('data/processed/populationSample7.csv', 'w') as f:
            writer = csv.writer(f)
            print(f"File is opened.")
            for sample in tqdm(results):
                row = []
                for i in range(1, len(self.probabilityDict.keys())+1):
                    row.append(str(sample[i]))
                writer.writerow(row)


    def generatePopulationSample(self, nArray):
        result = []
        for n in nArray:
            result.append(self.generatePersonSample(n))
        return result
    

    def generatePersonSample(self, n):
        wordsKnowledgeDict = {}
        for word in self.probabilityDict:
            # determine whether the person i knows the word
            probWord = self.probabilityDict[word]
            probKnowledge = self.getBinomDistribution(self.requieredOccurence-1, n, probWord)
            isKnown = self.getBernoulliSample(probKnowledge)
            wordsKnowledgeDict[word] = isKnown
        return wordsKnowledgeDict

           
    def estimateProbsOfWordOccurence(self, dict, totalCount):
        probDict = {}
        for key in dict:
            probDict[int(dict[key]["rank"])] = int(dict[key]["count"])/totalCount
        return probDict


    def getBinomDistribution(self, k, n, p):
        if n < 5000:
            return(1 - stats.binom.cdf(k, n, p))
        else:
            mean = n*p
            sd = math.sqrt(n*p*(1-p))
            z = (k-0.5-mean)/sd
            # P(X >= k) ~ P(Z >= z) where Z has approximatelly normal distribution
            return(1 - stats.norm.cdf(z))
    

    def getBernoulliSample(self, p):
        return np.random.binomial(1, p)


def main():
    ps = PopulationSample()
    ps.create()


if __name__ == "__main__":
    main()
