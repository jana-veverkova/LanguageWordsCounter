import re
import os

class WordExtractor:
    def __init__(self, directory):
        self.directory = directory


    def extractWords(self):
        languageDict = {}
        for filename in os.scandir(self.directory):
            if filename.is_file():
                languageDict = self.extractWordsFromFile(filename, languageDict)
        return languageDict


    # read txt file and convert to words, clean words - create dictionary of words 
    def extractWordsFromFile(self, filePath, languageDict):
        with open(filePath, encoding="utf-8") as file:
             for line in file:
                 for linePart in line.split():
                    word = self.getWord(linePart)
                    if word == "":
                        continue
                    if word in languageDict.keys():
                        languageDict[word] = languageDict[word]+1
                    else:
                        languageDict[word] = 1
        return languageDict


    def getWord(self, string):
        pattern = "^[\\W|\\d]*([A-Za-z]*[A-Za-z|'|’|-]*[A-Za-z]*)[\\W|\\d]*$"
        match = re.search(pattern, string.lower())
        if match:
            return match.group(1)
        else:
            return ""


def main():
    pass


if __name__ == "__main__":
    main()

