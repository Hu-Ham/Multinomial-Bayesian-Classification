"""
Multinomial Bayesian Classification Project
Authors:
Nathaniel Champion
Hugh Hamilton
Chris Beatrez
Andrew Kivrak

Description:
This program takes a json file and runs a bayesian classification calculation
on the data to algorithmically determine what classification each article would
be based on the title and short description provided. It will then compare what
the algorithm says is most likely and what the description actually is to
determine how well the calculation did.
"""
# Import libraries required for code to run
import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
import nltk

######################FUNCTIONS######################
"""
This Function takes a Category type and a Category list and combines
all the word counts. For example if there are two 'murder', '1' it deletes
one and makes it 'murder', '2' 
"""


def CatWords(Cat, dataSet):
    testWordList = []
    counter_1 = 0
    WordVar = []
    primeArray.clear()
    for x in dataSet:
        # print(len(listTest))
        if Cat in str(x):
            # print(counter_1)
            primeArray.append(listTest[counter_1])
        counter_1 += 1
    # print("top loop" + str(counter_1))
    counter_1 = 0
    for i in primeArray:
        # print(counter_1)
        #print("Primearray: " + str(i))
        for x in i:

            if x[0] not in stopWords:
                if x[0] not in testWordList:
                    #print('flag')
                    testWordList.append(x[0])
                    WordVar.append([x[0], 1])
                else:
                    #print("else value: " + str(x))
                    index = testWordList.index(x[0])
                    value_1 = WordVar[index][1]
                    WordVar[index] = ([x[0], (value_1 + 1)])
                    #print("after" + str(WordVar))
        counter_1 += 1


    return WordVar


"""
Counts the total number of words in the list
"""


def CatWordsCount(WordVar):
    count = 0
    for y in WordVar:
        count += y[1]
    return count


def compCat(wordVar):
    tempResults = []
    finalResults = []
    for i in listCheck:
        tempResults.clear()
        strResults = ''
        for z in i:
            for x in wordVar:
                tempWord = z[0]
                if tempWord == x[0]:
                    tempResults.append(x[1] / CrimeWordCount)
        for y in tempResults:
            strResults = strResults + " " + str(y)
        results = strResults[1:]
        finalResults.append([results])
    return finalResults


def probCat(Cat):
    probCategory = []
    for i in Cat:
        count = 0
        for x in listTest:
            tempData = str(x)
            if i in tempData:
                count += 1
        probCategory.append(count / len(testSet))

    return probCategory


# Importing in the json file that contains the data
data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

"""
These variables are use to cut the data set into 2 parts. The test data set is 20%
of the total dataset and will be used as reference. The checkset data set will be
80% of the original dataset and will have the bayesian calculation run on it to
determine each classification. The for loop will append each data element into a
list.
"""
CrimeWordCount = 0
testCount = round(.2 * len(data))
testSet = []
checkSet = []

for i in data[0:5000]:
    testSet.append(i)

for i in data[testCount + 1: testCount + 10000]:
    checkSet.append(i)

# These are the categories the dataset can be classified into
Categories = ['CRIME', 'ENTERTAINMENT', 'WORLD NEWS', 'IMPACT', 'POLITICS', 'WEIRD NEWS',
              'BLACK VOICES', 'WOMEN', 'COMEDY', 'QUEER VOICES', 'SPORTS', 'BUSINESS',
              'TRAVEL', 'MEDIA', 'TECH', 'RELIGION', 'SCIENCE', 'LATINO VOICES',
              'EDUCATION', 'COLLEGE', 'PARENTS', 'STYLE', 'GREEN', 'TASTE',
              'HEALTHY LIVING', 'WORLDPOST', 'GOOD NEWS', 'FIFTY', 'ARTS']
# List and variables needed to strip unnecessary information and tokenize each data element
headline = []
description = []
temp = ''
tempList = []
totalKeywords = []
counter = 0
tokenKeywords = []
keywords = []
finalKeywords = []

"""
This for loop strips out the information that is not the headline or short description part
of each data element and stores them in two separate lists. The next for loop concatenates
those two lists into one. And finally the third loop strips non-alphanumeric characters except
for spaces and then tokenizes the data element.
"""


def createDataSet(dataSet):
    counter_2 = 0
    for i in dataSet:
        temp = str(i)
        temp = temp.lower()
        tempList = temp.split("'headline':")
        temp = str(tempList[1])
        tempList = temp.split("'authors'")
        headline.append(tempList[0])
        tempList = temp.split("'short_description':")
        temp = str(tempList[1])
        tempList = temp.split("'date':")
        description.append(tempList[0])

    for i in range(0, len(dataSet)):
        totalKeywords.append(str(description[counter_2]) + str(headline[counter_2]))
        counter_2 += 1

    for i in totalKeywords:
        s = re.sub(r'[^A-Za-z ]+', '', i)
        tokenKeywords.append(word_tokenize(s))
    for i in stop_words:
        stopWords.append(i)

    counter_2 = 0

    for i in tokenKeywords:
        for x in i:
            if x in stopWords:
                tokenKeywords[counter_2].remove(str(x))
        counter_2 += 1

    checkList = []

    for i in tokenKeywords:
        freqDistro = nltk.FreqDist(i)
        checkList.append(list(freqDistro.most_common()))
    return checkList


stopWords = []
listTest = createDataSet(testSet)

listCheck = createDataSet(checkSet)

CrimeWords = []
primeArray = []

CrimeWords = CatWords(Categories[0], testSet)
CrimeWordCount = CatWordsCount(CrimeWords)
CrimeWords.sort()

CrimeResults = compCat(CrimeWords)

probArticleType = probCat(Categories)

##for i in CrimeResults[0:1]:
##    tempArray = []
##    tempArray = str(i).split(" ")
##    tempFloatArray = []
##    for x in tempArray:
##        value = None
##        numeric_string = re.sub("[^0-9.]", "", x)
##        value = float(numeric_string)
##        total = float(probArticleType[0])
##        tempFloatArray.append(value)
##    for i in tempFloatArray:
##        total = total * i
##print(testSet[0])
##print(listTest[0])
##print(CrimeWords)
##print(CrimeResults[0])
testingStr = "'category': 'CRIME', 'headline': 'There Were 2 Mass Shootings In Texas Last Week, But Only 1 On TV', 'authors':  " \
             "'link': 'https://www.huff89', 'short_description': 'She left her husband. He killed their children. Just another day in America.', 'date': '20'"
testingSet = []
for i in range(0, 10):
    testingSet.append(testingStr)

testingWords = CatWords(Categories[0], testingSet)

for i in CrimeResults:
    print(i)
