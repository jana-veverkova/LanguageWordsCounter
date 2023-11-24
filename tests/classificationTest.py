import src.model.classification as classification
import pandas as pd

def main():
    testFindNearestRatioIndex()
    testCalculateKnownWordsRation()
    testFindIndexesToTest()
    testFilterGroup()


def testFindNearestRatioIndex():
    cl = classification.Classification()

    assert cl.findNearestRatioIndex(pd.Series([0.5,0.4,0.3,0.2,0.1]), 0.2) == 3
    assert cl.findNearestRatioIndex(pd.Series([0.1,0.1,0.2,0.1,0.1]), 0.1) == 3
    assert cl.findNearestRatioIndex(pd.Series([0.9,0.8,0.9,0.6,0.7,0.5,0.5,0.4,0.3,0.4,0.2,0.1]), 0.65) == 3


def testCalculateKnownWordsRation():
    cl = classification.Classification()

    assert cl.calculateKnownWordsRation([1,1,1,1,1,1,1,1],[0,1,3,5,7]) == 1
    assert cl.calculateKnownWordsRation([0,0,0,0,0,0], [0,1,2,3,4,5]) == 0
    assert cl.calculateKnownWordsRation([0,0,0,1,1,1], [0,5]) == 1/2
    assert cl.calculateKnownWordsRation([0,1,1,0,0,1,1], [1,2,3,4,5,6]) == 4/6


def testFindIndexesToTest():
    cl = classification.Classification()

    assert len(cl.findIndexesToTest(100, 50, 10, [])[0]) == 10
    assert len(cl.findIndexesToTest(100, 50, 10, [])[1]) == 0
    assert len(cl.findIndexesToTest(0, 50, 10, [25])[1]) == 1
    assert len(cl.findIndexesToTest(50, 50, 10, [0,1,2,3,4,5,6,7,8,9])[1]) == 10


def testFilterGroup():
    cl = classification.Classification()

    df = [[1,0,0,0,0,0,0,0,0,0],
          [1,1,0,0,0,0,0,0,0,0],
          [1,1,1,0,0,0,0,0,0,0],
          [1,1,1,1,0,0,0,0,0,0],
          [1,1,1,1,1,0,0,0,0,0],
          [1,1,1,1,1,1,0,0,0,0],
          [1,1,1,1,1,1,1,0,0,0],
          [1,1,1,1,1,1,1,1,0,0],
          [1,1,1,1,1,1,1,1,1,0],
          [1,1,1,1,1,1,1,1,1,1]]
    
    assert len(cl.filterGroup(pd.DataFrame(df), 5, 2, 0.99, 1)[0]) == 3
    assert len(cl.filterGroup(pd.DataFrame(df), 0, 2, 1/3-0.01, 2/3+0.01)[0]) == 2
    assert len(cl.filterGroup(pd.DataFrame(df), 5, 2, 3/5, 1)[0]) == 5    
    assert len(cl.filterGroup(pd.DataFrame(df), 5, 2, 0, 1)[0]) == 10 
    assert len(cl.filterGroup(pd.DataFrame(df), 5, 2, (1/5)-0.01, (1/5)+0.01)[0]) == 1

if __name__ == "__main__":
    main()