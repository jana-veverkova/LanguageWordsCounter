import src.data.wordExtractor as we
import csv

class FrequencyDictionary:
    def __init__(self):
        pass


    # create frequency dictionary and save as csv
    def create(self, directory):
        languageDict = we.WordExtractor(directory).extractWords()

        # save to csv
        with open('data/processed/dictionary.csv', 'w') as f:
            writer = csv.writer(f)

            count = 0
            sortedDictionary = sorted(languageDict.items(), key=lambda x:x[1], reverse=True)
            for ix, item in enumerate(sortedDictionary):                
                row = [str(ix+1), str(item[0]), str(item[1])]
                writer.writerow(row)
                count = count + 1
                if count == 50000:
                    break
    
 
    def getByWord(self):
        dict = {}
        totalCount = 0
        with open('data/processed/dictionary.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    dict[row[1]] = {"rank": row[0], "count": row[2]}
                    totalCount = totalCount + int(row[2])
        return dict, totalCount
    

    def getByRank(self):
        dict = {}
        with open('data/processed/dictionary.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1:
                    dict[row[0]] = row[1]
        return dict


def main():
    fd = FrequencyDictionary()
    fd.create("data/original")


if __name__ == "__main__":
    main()
