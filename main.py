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
the algorithm says is most likely and what the desription actually is to
determine how well the calculation did.
"""
#Import libraries required for code to run
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
def CatWords(Cat, WordVar):
    testWordList = []
    counter = 0
    catList = 0
    for x in testSet:
        if Cat in str(x):
            primeArray.append(listTest[counter])
        counter += 1
    counter = 0
    
    
    for i in primeArray:
        for x in i:
            if x[0] not in stopWords:
                if x[0] not in testWordList:
                    testWordList.append(x[0])
                    WordVar.append([x[0], 1])
                else:
                    for y in WordVar:
                        if x[0] == y[0]:
                            WordVar.remove(y)
                            WordVar.append([x[0], (x[1]+1)])     
    primeArray.clear()
"""
Counts the total number of words in the list
"""
def CatWordsCount(Cat, WordVar):
    count = 0
    for y in WordVar:
        count += y[1]
    return count


def compCat(wordVar):
    counter = 0
    tempResults = []
    finalResults = []
    strResults = ''
    for i in listCheck:
        tempResults.clear()
        strResults = ''
        for z in i:
            for x in wordVar:
                tempWord = z[0]
                if tempWord == x[0]:
                    tempResults.append(x[1]/CrimeWordCount)    
        for i in tempResults:
            strResults = strResults + " " + str(i)
        results = strResults[1:]
        finalResults.append([results])
    return(finalResults)
def probCat(Cat):
    probCat = []
    for i in Cat:
        count = 0
        for x in listTest:
            tempData = str(x)
            if i in tempData:
                count += 1
        probCat.append(count/len(testSet))

    return(probCat)

#Importing in the json file that contains the data
data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

"""
These variables are use to cut the data set into 2 parts. The test data set is 20%
of the total dataset and will be used as reference. The checkset data set will be
80% of the original dataset and will have the bayesian calculation run on it to
determine each classification. The for loop will append each data element into a
list.
"""
CrimeWordCount = 0
testCount = round(.2*len(data))
testSet = []
checkSet = []

for i in data[0:testCount]:
    testSet.append(i)
    
for i in data[testCount+1: ]:
    checkSet.append(i)

#These are the categories the dataset can be classified into
Categories = ['CRIME', 'ENTERTAINMENT', 'WORLD NEWS', 'IMPACT', 'POLITICS', 'WEIRD NEWS',
              'BLACK VOICES', 'WOMEN', 'COMEDY', 'QUEER VOICES', 'SPORTS', 'BUSINESS',
              'TRAVEL', 'MEDIA', 'TECH', 'RELIGION', 'SCIENCE', 'LATINO VOICES',
              'EDUCATION', 'COLLEGE', 'PARENTS', 'STYLE', 'GREEN', 'TASTE',
              'HEALTHY LIVING', 'WORLDPOST', 'GOOD NEWS', 'FIFTY', 'ARTS']
#List and variables needed to strip unnecessary information and tokenize each data element
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
##for i in testSet:
##    temp = str(i)
##    temp = temp.lower()
##    tempList = temp.split("'headline':")
##    temp = str(tempList[1])
##    tempList = temp.split("'authors'")
##    headline.append(tempList[0])
##    tempList = temp.split("'short_description':")
##    temp = str(tempList[1])
##    tempList = temp.split("'date':")
##    description.append(tempList[0])
##
##for i in range(0, len(testSet)):
##    totalKeywords.append(str(description[counter]) + str(headline[counter]))
##    counter += 1 
##
##stopWords = []
##
##for i in totalKeywords:
##    s = re.sub(r'[^A-Za-z ]+', '', i)
##    tokenKeywords.append(word_tokenize(s))
##for i in stop_words:
##    stopWords.append(i)
##
##counter = 0
##
##for i in tokenKeywords:
##    for x in i:
##        if x in stopWords:
##            tokenKeywords[counter].remove(str(x))
##    counter += 1
##
##
##
##
##for i in tokenKeywords:
##    freqDistro = nltk.FreqDist(i)
##    commonList.append(list(freqDistro.most_common()))
##
##primeArray = []
   

def set(set):
    counter = 0
    for i in set:
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

    for i in range(0, 100):
        totalKeywords.append(str(description[counter]) + str(headline[counter]))
        counter += 1 



    for i in totalKeywords:
        s = re.sub(r'[^A-Za-z ]+', '', i)
        tokenKeywords.append(word_tokenize(s))
    for i in stop_words:
        stopWords.append(i)

    counter = 0

    for i in tokenKeywords:
        for x in i:
            if x in stopWords:
                tokenKeywords[counter].remove(str(x))
        counter += 1


    checkList = []

    for i in tokenKeywords:
        freqDistro = nltk.FreqDist(i)
        checkList.append(list(freqDistro.most_common()))
    return checkList

stopWords = []
listTest = set(testSet)
listCheck = set(checkSet)
counter = 0
CrimeWords = []
primeArray = []

CatWords(Categories[0], CrimeWords)
CrimeWordCount = CatWordsCount(Categories[0], CrimeWords)
CrimeWords.sort()


CrimeResults = compCat(CrimeWords)
counter = 0


probArticleType = probCat(Categories)
total = 0
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
print(testSet[0])
print(listTest[0])
print(CrimeWords)
print(CrimeResults[0])

