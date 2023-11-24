import pandas as pd
import numpy as np
import math
from tqdm import tqdm

class Classification:
    def __init__(self):    
        pass

    def setTrainSet(self, trainSet):
        self.trainSet = trainSet

    
    def setRadius(self, radius):
        self.radius = radius

    
    def setWordsAskedNum(self, num):
        self.wordsAskedNum = num

    
    def setMaximalGuessRange(self, dev):
        self.guessRange = dev


    def classify(self, observation):
        testedWords = []
        iterations = []
        groupIntersection = self.trainSet.index.values

        group = self.trainSet
        iterate = True
        iterCount = 0
        min = 0
        max = 0
         
        while(iterate and iterCount < 11):
            subgroup = self.runClassificationIteration(group, observation, self.radius, self.wordsAskedNum, testedWords)
            testedWords = np.concatenate((testedWords,subgroup["newTestedWords"]))

            for iter in iterations:
                iter = self.findNearestSubgroup(self.trainSet, observation, iter["centerIx"], self.radius, testedWords)
                groupIntersection = self.intersection(groupIntersection, iter["groupIxs"])

            iterations.append(subgroup)
            groupIntersection = self.intersection(groupIntersection, subgroup["groupIxs"])
            finalGroup = group.loc[groupIntersection]
            finalGroupRowSums = pd.DataFrame(finalGroup.sum(axis=1))
            max = finalGroupRowSums.max()[0]
            min = finalGroupRowSums.min()[0]

            if (max - min < self.guessRange):
                iterate = False
            else:
                group = finalGroup

            iterCount = iterCount + 1

        return min, max


    def runClassificationIteration(self, group, observation, radius, wordsToTestNum, testedWords):
        ratioSeries = group.sum(axis=0)/len(group)
        centerIx = self.findNearestRatioIndex(ratioSeries, 0.5)
        indexesToTest, testedIndexes = self.findIndexesToTest(centerIx, radius, wordsToTestNum, testedWords)
        subgroup = self.findNearestSubgroup(group, observation, centerIx, radius, np.concatenate((np.array(indexesToTest), np.array(testedIndexes))))
        subgroup["newTestedWords"] = indexesToTest
        return subgroup


    def findNearestSubgroup(self, group, observation, centerIx, radius, testedWords):
        testedWordsInRange = [num for num in testedWords if (num >= centerIx - radius) & (num <= centerIx + radius)]
        wordsKnownRatio = self.calculateKnownWordsRation(observation, testedWordsInRange)
        se = math.sqrt(wordsKnownRatio*(1-wordsKnownRatio)/len(testedWordsInRange))
        lowerInterval = wordsKnownRatio - 2*se - 0.01
        upperInterval = wordsKnownRatio + 2*se + 0.01
        gr = self.filterGroup(group, centerIx, radius, lowerInterval, upperInterval)

        result = { 
            'centerIx': centerIx,
            'pHat': wordsKnownRatio,
            'seHat': se,
            'lowerInterval': lowerInterval, 
            'upperInterval': upperInterval,
            'newTestedWords': 0,
            'groupIxs': gr[0],
            'group': gr[1]}
        
        return result


    def filterGroup(self, group, centerIx, radius, lowerInterval, upperInterval):
        a = max(centerIx-radius,0)
        b = min(centerIx+radius,50000)

        filtered = group.loc[(group.iloc[:,a:b+1].sum(axis=1)/(b-a+1) >= lowerInterval) & (group.iloc[:,a:b+1].sum(axis=1)/(b-a+1) <= upperInterval)]
        return filtered.index.values, filtered


    def calculateKnownWordsRation(self, observation, indexesToTest):
        count = 0

        for i in indexesToTest:
            if (observation[i] == 1) :
                count = count + 1

        return count/len(indexesToTest)


    def findIndexesToTest(self, ix, radius, num, testedWords):
        a = max(ix-radius,0)
        b = min(ix+radius,50000)
        indexesForTest = range(a, b+1, 1)
        indexesForTestFinal = []
        testedIndexes = []

        for i in indexesForTest:
            if pd.Series(i).isin(testedWords)[0] == False:
                indexesForTestFinal.append(i)
            else:
                testedIndexes.append(i)

        return np.random.choice(indexesForTestFinal, num), testedIndexes
    
    
    def findNearestRatioIndex(self, ratioSeries, ratio):
        centerIx = 0
        rounds = 0
        rat = 100
        a = 0
        b = len(ratioSeries) - 1
        roundsLim = 100

        while centerIx == 0 and rounds <= roundsLim:
            c = a + int((b-a)/2)
            if abs(ratioSeries[c] - ratio) < abs(rat - ratio):
                rat = ratioSeries[c]

            if ratioSeries[c] > ratio:
                a = c
            elif ratioSeries[c] < ratio:
                b = c
            else:
                centerIx = c

            if rounds == roundsLim:
                aDist = abs(ratioSeries[a] - ratio)
                bDist = abs(ratioSeries[b] - ratio)
                cDist = abs(ratioSeries[c] - ratio)
                closest = min(aDist, bDist, cDist)
                if closest == aDist:
                    centerIx = a
                elif closest == bDist:
                    centerIx = b
                else: centerIx = c                
                
            rounds = rounds + 1

        return centerIx
                

    def intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3
    

def main():
    pass
    trainFile = "data/train/train.csv"
    testFile = "data/train/test.csv"

    train = pd.read_csv(trainFile, header = None)
    test = pd.read_csv(testFile, header = None)

    clas = Classification()
    clas.setTrainSet(train)
    clas.setRadius(1000)
    clas.setWordsAskedNum(10)
    clas.setMaximalGuessRange(1000)

    rows_list = []

    for i in tqdm(range(100)):
        obs1 = test.iloc[i]
        res = clas.classify(obs1)
        guessed = obs1.sum() >= res[0] and obs1.sum() <= res[1]
        dict1 = {
            "observation": i,
            "words_knows": obs1.sum(),
            "guessed_min": res[0],
            "guessed_max": res[1],
            "guessed:": guessed
        }
        rows_list.append(dict1)

    df = pd.DataFrame(rows_list)
    df.to_csv('data/train/results1.csv')


if __name__ == "__main__":
    main()