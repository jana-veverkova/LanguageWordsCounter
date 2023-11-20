import pandas as pd
from sklearn.model_selection import train_test_split
import csv
from p_tqdm import p_map, p_umap, p_imap, p_uimap

class TrainTestSplit:
    def __init__(self):
        pass


    def split(self):
        sampleFile1 = "data/processed/populationSample1.csv"
        sampleFile2 = "data/processed/populationSample2.csv"
        sampleFile3 = "data/processed/populationSample3.csv"
        sampleFile4 = "data/processed/populationSample4.csv"
        sampleFile5 = "data/processed/populationSample5.csv"
        sampleFile6 = "data/processed/populationSample6.csv"
        sampleFile7 = "data/processed/populationSample7.csv"

        sample1 = pd.read_csv(sampleFile1, header = None)
        sample2 = pd.read_csv(sampleFile2, header = None)
        sample3 = pd.read_csv(sampleFile3, header = None)
        sample4 = pd.read_csv(sampleFile4, header = None)
        sample5 = pd.read_csv(sampleFile5, header = None)
        sample6 = pd.read_csv(sampleFile6, header = None)
        sample7 = pd.read_csv(sampleFile7, header = None)

        sample = pd.concat([sample1, sample2, sample3, sample4, sample5, sample6, sample7])
        
        train, test = train_test_split(sample, test_size=0.2, random_state=0)

        print(len(train))
        print(len(train.columns))
        print(len(test))
        print(len(test.columns))

        train.to_csv('data/train/train.csv')
        test.to_csv('data/train/test.csv')

    
def main():
    tts = TrainTestSplit()
    tts.split()


if __name__ == "__main__":
    main()