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
    primeArray = []
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
        # print("Primearray: " + str(i))
        for x in i:

            if x[0] not in stopWords:
                if x[0] not in testWordList:
                    # print('flag')
                    testWordList.append(x[0])
                    WordVar.append([x[0], 1])
                else:
                    # print("else value: " + str(x))
                    index = testWordList.index(x[0])
                    value_1 = WordVar[index][1]
                    WordVar[index] = ([x[0], (value_1 + 1)])
                    # print("after" + str(WordVar))
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


def compCat(wordVar, wordCount):
    finalResults = []
    successCounter = 0
    for i in listCheck[0:12]:
        tempWord = ""
        tempResults = []
        counter_2 = 0
        tempCheckList = []
        for z in i:
            tempCheckList.append(z[0])
            for x in wordVar:
                tempWord = tempCheckList[counter_2]
                # print("article word" + str(tempWord))
                # print("category word" + str(x[0]))
                if tempWord == x[0]:
                    tempResults.append([x[0], (x[1] / wordCount)])
                    successCounter = 1
            if successCounter == 0:
                tempResults.append([tempWord, (1 / wordCount)])
            successCounter = 0
            counter_2 += 1
        finalResults.append(tempResults)
    return finalResults


def probCat(Cat):
    probCategory = []
    for i in Cat:
        count = 0
        for x in testSet:

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
testCount = round(.3 * len(data))
testSet = []
checkSet = []

for i in data[0:testCount]:
    testSet.append(i)

for i in data[testCount + 1:testCount + 100]:
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


allCatCounter = 0
AllCatWords = []
for i in Categories:
    tempResults_1 = CatWords(Categories[allCatCounter], testSet)
    AllCatWords.append(tempResults_1)
    allCatCounter += 1
AllCatWordCounts = []
for i in AllCatWords:
    AllCatWordCounts.append(CatWordsCount(i))

AllCatResults = []
allCatCounter = 0
for i in Categories:
    tempResults_2 = compCat(AllCatWords[allCatCounter], AllCatWordCounts[allCatCounter])
    AllCatResults.append(tempResults_2)
    allCatCounter += 1

probArticleType = probCat(Categories)

testCounter = 0
total = 0
resultsRecord = []
res = []

catRes = []
for i in AllCatResults:
    print(i)
    res.clear()
    for z in i:
        calcValue = probArticleType[testCounter]
        print("Prob Article: " + str(calcValue))
        for y in z:
            calcValue = calcValue * y[1]
        res.append(calcValue)
    catRes.append(res[:])
    print("Results: " + str(res))
    testCounter += 1
counter = 0
tempRes = []
wordRes = []
counter_3 = 0
for x in range(len(catRes[0])):
    for i in catRes:
        tempValue = i[counter_3]
        tempRes.append(tempValue)
    wordRes.append(tempRes[:])
    tempRes.clear()
    counter_3 += 1

finalResult = []
for i in wordRes:
    finalResult.append([i.index(max(i)), max(i)])
print(testSet[0])

counter = 0
for i in finalResult:
    print(i)
    print(Categories[i[0]])
    print(AllCatResults[counter])
    if Categories[i[0]] in AllCatResults[counter]:
        print('flag')
        TotalTotal += 1
        finalArray[i[0]] += 1
    counter += 1
print(finalArray)
