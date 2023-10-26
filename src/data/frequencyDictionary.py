import wordExtractor as we
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

            sortedDictionary = sorted(languageDict.items(), key=lambda x:x[1], reverse=True)
            for item in sortedDictionary:
                row = [item[0], item[1]]
                writer.writerow(row)
    

    def get(self):
        dict = {}
        totalCount = 0
        with open('data/processed/dictionary.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                dict[row[0]] = row[1]
                totalCount = totalCount + int(row[1])
        return dict, totalCount


def main():
    pass


if __name__ == "__main__":
    main()
