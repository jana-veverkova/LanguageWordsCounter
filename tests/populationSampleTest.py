import src.data.populationSample as populationSample

def main():
    testEstimateProbsOfWordOccurence()
    testGetBinomDistribution()


def testEstimateProbsOfWordOccurence():
    ps = populationSample.PopulationSample()

    dict1 = {"word1": 1, "word2": 9}
    dict2 = {"word1": 0, "word2": 9}    
    dict3 = {"word1": 5, "word2": 5, "word3": 5}
    dict4 = {"word1": 5}
    assert ps.estimateProbsOfWordOccurence(dict1, 10)["word1"] == 1/10
    assert ps.estimateProbsOfWordOccurence(dict1, 10)["word2"] == 9/10
    assert ps.estimateProbsOfWordOccurence(dict2, 9)["word1"] == 0
    assert ps.estimateProbsOfWordOccurence(dict2, 9)["word2"] == 1
    assert ps.estimateProbsOfWordOccurence(dict3, 15)["word1"] == 5/15
    assert ps.estimateProbsOfWordOccurence(dict3, 15)["word3"] == 5/15
    assert ps.estimateProbsOfWordOccurence(dict4, 5)["word1"] == 1


def testGetBinomDistribution():
    ps = populationSample.PopulationSample()

    assert round(ps.getBinomDistribution(11,50,0.3), 3) == 0.921
    assert round(ps.getBinomDistribution(41,100,0.5), 3) == 0.972


if __name__ == "__main__":
    main()