import sys
import src.data.wordExtractor as wordExtractor

def main():
    testWordExtractor()
    testExtractWordsFromFile()


def testWordExtractor():
    we = wordExtractor.WordExtractor("data/test")

    assert we.getWord("abc") == "abc"
    assert we.getWord("Hello!") == "hello"    
    assert we.getWord("!Hello") == "hello"
    assert we.getWord("sour-milk")== "sour-milk"    
    assert we.getWord("-milk")== "milk"    
    assert we.getWord("2hello")=="hello"
    assert we.getWord("b2b")==""
    assert we.getWord("HELLO2")=="hello"
    assert we.getWord("1.Hello...")=="hello"
    assert we.getWord("1.hello...")=="hello"
    assert we.getWord("\"comment\"")=="comment"    
    assert we.getWord("(comment)")=="comment"
    assert we.getWord("it’s")=="it’s"
    assert we.getWord("")==""
    assert we.getWord("123")==""


def testExtractWordsFromFile():
    we = wordExtractor.WordExtractor("data/test")

    assert we.extractWordsFromFile("data/test/test1.txt", {})["tour"] == 1
    assert "1998" not in we.extractWordsFromFile("data/test/test1.txt", {})
    assert "100-year-old" not in we.extractWordsFromFile("data/test/test1.txt", {})
    assert "year" not in we.extractWordsFromFile("data/test/test2.txt", {})
    assert we.extractWordsFromFile("data/test/test2.txt", {})["a"] == 2
    assert we.extractWordsFromFile("data/test/test2.txt", {})["titanic"] == 1
    assert we.extractWordsFromFile("data/test/test3.txt", {})["page"] == 1
    assert we.extractWordsFromFile("data/test/test3.txt", {})["on-line"] == 1
    assert we.extractWordsFromFile("data/test/test3.txt", {})["a"] == 2
    assert we.extractWordsFromFile("data/test/test3.txt", {})["living"] == 1
    assert we.extractWordsFromFile("data/test/test3.txt", {})["years"] == 1
    assert we.extractWordsFromFile("data/test/test4.txt", {})["band's"] == 1
    assert we.extractWordsFromFile("data/test/test4.txt", {})["graffiti"] == 1
    assert we.extractWordsFromFile("data/test/test4.txt", {})["they’d"] == 1
    assert we.extractWordsFromFile("data/test/test4.txt", {})["the"] == 2
    assert we.extractWordsFromFile("data/test/test5.txt", {})["attacks"] == 2
    assert we.extractWordsFromFile("data/test/test5.txt", {})["happen"] == 2
    assert we.extractWordsFromFile("data/test/test5.txt", {})["again"] == 2
    assert we.extractWordsFromFile("data/test/test5.txt", {})["suddenly"] == 1
    assert "Քաշաթաղի" not in we.extractWordsFromFile("data/test/test6.txt", {})
    assert "melikdom" not in we.extractWordsFromFile("data/test/test6.txt", {})
    assert we.extractWordsFromFile("data/test/test6.txt", {})["xv-xvii"] == 1

if __name__ == "__main__":
    main()