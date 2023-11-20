import pandas as pd
import numpy as np
import math

class Classification:
    def __init__(self):    
        pass

    def setTrainSet(self, trainSet):
        self.trainSet = trainSet

    
    def setRadius(self, radius):
        self.radius = radius

    
    def setWordsAskedNum(self, num):
        self.wordsAskedNum = num

    
    def setMaximalDeviation(self, dev):
        self.dev = dev


    def classify(self, observation):
        testedWords = []
        iterations = []
        groupIntersection = self.trainSet

        group = self.trainSet
        iterate = True
        while(iterate):
            subgroup = self.runClassificationIteration(group, observation, self.radius, self.wordsAskedNum, testedWords)
            testedWords.append(subgroup.newTestedWords)

            for ix, iter in iterations:
                iter = self.findNearestSubgroup(self.trainSet, observation, iter.centerIx, self.radius, testedWords)
                groupIntersection = self.intersection(groupIntersection, iter.group.index.values)

            iterations.append(subgroup)
            groupIntersection = self.intersection(groupIntersection, subgroup.group.index.values)

            finalGroup = group.loc[groupIntersection]
            finalGroupRowSums = pd.DataFrame(finalGroup.sum(axis=1))
            if (max(finalGroupRowSums) - min(finalGroupRowSums) < 10):
                iterate = False
                return min(finalGroupRowSums), max(finalGroupRowSums)
            else:
                group = finalGroup





    def runClassificationIteration(self, group, observation, radius, wordsToTestNum, testedWords):
        ratioSeries = group.sum()/len(group)
        centerIx = self.findNearestRatioIndex(ratioSeries, 0.5)
        indexesToTest, testedIndexes = self.findIndexesToTest(centerIx, radius, wordsToTestNum, testedWords)
        subgroup = self.findNearestSubgroup(group, observation, centerIx, radius, np.concatenate(indexesToTest, testedIndexes))
        subgroup.newTestedWords = indexesToTest
        return subgroup


    def findNearestSubgroup(self, group, observation, centerIx, radius, testedWords):
        testedWordsInRange = testedWords[(testedWords >= centerIx - radius) & (testedWords <= centerIx + radius)]
        wordsKnownRatio = self.calculateKnownWordsRation(observation, testedWordsInRange)
        se = math.sqrt(wordsKnownRatio*(1-wordsKnownRatio)/len(testedWordsInRange))
        lowerInterval = len(testedWordsInRange) - 2*se
        upperInterval = len(testedWordsInRange) + 2*se
        result = { 
            'centerIx': centerIx,
            'pHat': wordsKnownRatio,
            'seHat': se,
            'lowerInterval': lowerInterval, 
            'upperInterval': upperInterval,
            'newTestedWords': 0,
            'group': self.filterGroup(group, centerIx, radius, lowerInterval, upperInterval)}
        return result


    def filterGroup(self, group, centerIx, radius, lowerInterval, upperInterval):
        filteredGroup = pd.DataFrame()
        a = max(centerIx-radius,0)
        b = min(centerIx+radius,50000)
        cols = group.iloc[:,a:b+1]
        sums = pd.DataFrame(cols.sum(axis=1))
        selected = sums.loc[(sums.iloc[:,0]/(b-a+1) >= lowerInterval) & (sums.iloc[:,0]/(b-a+1) <= upperInterval)]
        return group.iloc[selected.index.values]


    def calculateKnownWordsRation(self, observation, indexesToTest):
        count = 0
        for i in indexesToTest:
            if observation[i] == 1:
                count = count + 1
        return count/len(indexesToTest)


    def findIndexesToTest(self, ix, radius, num, testedWords):
        a = max(ix-radius,0)
        b = min(ix+radius,50000)
        indexesForTest = range(a, b+1, 1)
        indexesForTestFinal = []
        numFinal = num
        testedIndexes = []
        for i in indexesForTest:
            if i not in testedWords:
                indexesForTestFinal.append(i)
            else:
                testedIndexes.append(i)
                numFinal = numFinal - 1
        return np.random.choice(indexesForTestFinal, numFinal), testedIndexes
    
    
    def findNearestRatioIndex(self, ratioSeries, ratio):
        centerIx = 0
        rounds = 0
        rat = 100
        a = 0
        b = len(ratioSeries) - 1
        roundsLim = 100
        while centerIx == 0 and rounds <= roundsLim:
            c = a + int((b-a)/2)
            print(f"{rounds} {rat} {a} {c} {b}")
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
                

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3




    # set nearestNeighbors = trainSet
    # find middle of nearestNeighbors
    # set set of tested words as middle +- radius
    # test randomly n words in tested set
    # calculate ratio of known words
    # calculate confidence interval
    # if ration == 0.5 => ask next 2 words and repeat
    # if ratio <> 0.5 
    ## get items from trainSet with ratio inside confidence interval and set nearestNeighbors as these items
    ## estimates words known
    ## if words known is <

def main():
    pass
    #trainFile = "data/train/train.csv"
    #testFile = "data/test/test.csv"

    #train = pd.read_csv(trainFile, header = None)
    #test = pd.read_csv(testFile, header = None)

    #clas = Classification()
    #clas.setMaximalDeviation(1000)
    #clas.classify(test.head(1))


if __name__ == "__main__":
    main()