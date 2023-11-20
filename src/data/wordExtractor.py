import re
import os
from datetime import datetime

class WordExtractor:
    def __init__(self, directory):
        self.directory = directory


    def extractWords(self):
        print(datetime.now())
        languageDict = {}
        for filename in os.scandir(self.directory):
            if filename.is_file():
                print(f"Processing {filename} ... \n")
                result = self.extractWordsFromFile(filename)
                languageDict = self.processResults(languageDict, result)
                print(f"{filename} is processed.\n")
        print(datetime.now())
        return languageDict


    # read txt file and convert to words, clean words - create dictionary of words 
    def extractWordsFromFile(self, filePath):
        result = {}
        with open(filePath, encoding="utf-8") as file:
             for line in file:
                 result = self.processResults(result, self.extractWordsFromLine(line))
        return result


    def extractWordsFromLine(self, line):
        result = {}
        for linePart in line.split():
            word = self.getWord(linePart)
            if word == "":
                continue
            if word in result.keys():
                result[word] = result[word]+1
            else:
                result[word] = 1
        return result
    

    def processResults(self, dict, result):
        for word in result:
            if word in dict.keys():
                dict[word] = dict[word] + result[word]
            else:
                dict[word] = result[word]
        return dict


    def getWord(self, string):
        pattern = "^[\\W|\\d]*([a-zA-Z]+(?:['’-][a-zA-Z]+)?)[\\W|\\d]*$"
        match = re.search(pattern, string.lower())
        if match:
            return match.group(1)
        else:
            return ""


def main():
    we = WordExtractor("data/original")
    we.extractWords()


if __name__ == "__main__":
    main()

