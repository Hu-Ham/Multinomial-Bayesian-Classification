from time import time

start = time()
"""Multinomial Bayesian Classification Project
Authors:
Nathaniel Champion
Hugh Hamilton
Chris Beatrez
Andrew Kivrak
Description:
This program takes a JSON file and runs a bayesian classification calculation
on the data to algorithmically determine what classification each article would
be based on the title and short description provided. It will then compare what
the algorithm says is most likely and what the description actually is to
determine how well the calculation performed."""
# Import libraries required for code to run
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# These are the categories the dataset can be classified into. In global scope, not subject to change
CATEGORIES = ('CRIME', 'ENTERTAINMENT', 'WORLD NEWS', 'IMPACT', 'POLITICS', 'WEIRD NEWS',
              'BLACK VOICES', 'WOMEN', 'COMEDY', 'QUEER VOICES', 'SPORTS', 'BUSINESS',
              'TRAVEL', 'MEDIA', 'TECH', 'RELIGION', 'SCIENCE', 'LATINO VOICES',
              'EDUCATION', 'COLLEGE', 'PARENTS', 'STYLE', 'GREEN', 'TASTE',
              'HEALTHY LIVING', 'WORLDPOST', 'GOOD NEWS', 'FIFTY', 'ARTS')
######################FUNCTIONS######################

"""This function cleans and tokenizes the raw data from the JSON file"""
def createDataSet(dataSet):
    """These for loops strip out the parts of the JSON data that are not the headline or short article
    descriptions, remove all non alphabetical (or space) characters, tokenize all words as list entries
    and then reference them to a list of stop words expanded for non-apostrophized English."""
    allCleanTokens = [] #The list of all clean word tokens to be produced
    #We expand the number of stop words to include variations missing apostrophes
    stop_words = nltk.corpus.stopwords.words("english")
    tokenSW = nltk.corpus.stopwords.words("english")
    for i in stop_words:
        s = re.sub(r'[^A-Za-z ]+', '', i)
        tokenSW.append(s)
    for row in dataSet:
        dataString = str(row).lower() #Cast all JSON table rows to lowercase string
        #Remove all of the string prior to the headline, including article category:
        splitString = dataString.split("'headline':")
        dataString = str(splitString[1])
        #Split along authors and append headline substring to headline list
        splitString = dataString.split("'authors'")
        #Non alphabetical or space characters removed, and then all words added to wordTokens list
        alphaString = splitString[0].replace("-", " ") #Also replace all dashes with spaces
        alphaString = re.sub("[^a-zA-Z ]+", "", alphaString)
        wordTokens = word_tokenize(alphaString)
        #Remove the string portion before the short description substring
        splitString = dataString.split("'short_description':")
        dataString = str(splitString[1])
        #Split to isolate the short description substring from the "date:" substring
        splitString = dataString.split("'date':")
        #Now reallocate alphabetical string with this string subsection, and add to token list
        alphaString = splitString[0].replace("-", " ")
        alphaString = re.sub("[^a-zA-Z ]+", "", alphaString)
        wordTokens += word_tokenize(alphaString)
        cleanTokens = [token for token in wordTokens if not token in tokenSW]
        allCleanTokens.append(cleanTokens)
    checkList = []
    for i in allCleanTokens:
        freqDistro = nltk.FreqDist(i)
        checkList.append(list(freqDistro.most_common()))
    return checkList

"""This function takes a type denoting the  and a Category list and combines
all the word counts. For example if there are two articles that mention
'murder', then it will update to 'murder', 2 in the array."""

def CatWords(Cat, dataSet):
    # Creating necessary variables
    testWordList = []
    counter_1 = 0
    WordVar = []
    finalWordVar = []
    primeArray = []
    # For loop to iterate through the articles we are calculating
    for x in dataSet:
        """ If the article is equal to the compared category it
        appends it to the testing list element that corresponds
        to that category. Once it compares all the articles to 
        a category the counter goes up and will then compare it
        to the next category and add the value to that categories
        element in listTest array.
        """
        if Cat in str(x):
            primeArray.append(listTest[counter_1])
        counter_1 += 1
    counter_1 = 0
    """ Now that we have an array that has all the words for each 
    category we compare them to stopWords to remove unimportant words
    to reduce the number of comparison and improve the accuracy. If the
    word appears a second time in a different article instead of adding
    the word it will increment the number of occurrences instead.
    """
    for i in primeArray:
        for x in i:
            if x[0] not in stopWords:
                if x[0] not in testWordList:
                    testWordList.append(x[0])
                    WordVar.append([x[0], 1])
                else:
                    index = testWordList.index(x[0])
                    value_1 = WordVar[index][1]
                    WordVar[index] = ([x[0], (value_1 + 1)])
        counter_1 += 1
    for i in WordVar:
        if i[1] != 1:
            finalWordVar.append(i)
    # Returns the updated array
    return finalWordVar

"""Counts the total number of words in the list and returns
with the total number for each category."""

def CatWordsCount(WordVar):
    count = 0
    for y in WordVar:
        count += y[1]
    return count

"""Function that takes in the array with the list of words
and a total word count. It then compares the words in the 
specific article we are comparing to the list of words in 
each category and produces a % for the likelihood of it 
being that article based on the number of time the word 
appeared in that category and the total number of words."""

def compCat(wordVar, wordCount):
    # Creates variable required for function
    finalResults = []
    successCounter = 0
    """listCheck is the array that contains the keyword for 
    each article in a element within that array"""
    for i in listCheck:
        tempWord = ""
        tempResults = []
        counter_2 = 0
        tempCheckList = []
        """the variable i is an array of tuples ex: [('word', 1), 
        ('word2', 1)] z would then just be a single tuple ('word', 1)
         and then z[0] would just be the 'word' which is appended in the 
         tempCheckList variable."""
        for z in i:
            tempCheckList.append(z[0])
            """Takes value in the above list and compares it to each value
            in the list of words in each category. If it finds the word it
            adds a tuple that includes the word and the probability. If it
            does not find the word in that list it then provides the probability
            of the word appearing a single time. This is our smoothing code"""
            for x in wordVar:
                tempWord = tempCheckList[counter_2]
                #print("article word" + str(tempWord))
                #print("category word" + str(x[0]))
                if tempWord == x[0]:
                    tempResults.append([x[0], (x[1] / wordCount)])
                    successCounter = 1
            if successCounter == 0 & wordCount != 0:
                tempResults.append([tempWord, (1 / wordCount)])
            successCounter = 0
            counter_2 += 1
        finalResults.append(tempResults)
        # returns array with the probability for each word in an article
    return finalResults

"""Function that determines the probability of each category.
ex: if there is 1 crime article and 10 total articles then
the probability of it being a crime article is 10%."""

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

#Beginning of program execution: 
# Importing in the JSON file that contains the data
data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

"""These variables are use to cut the data set into 2 parts. The test data set is 80%
of the total dataset and will be used as reference. The checkset data set will be
20% of the original dataset and will have the bayesian calculation run on it to
determine each classification. The for loop will append each data element into a
list."""
testCount = 100
#testCount = round(.8 * len(data))
testSet = []
checkSet = []

for i in data[0:testCount]:
    testSet.append(i)

for i in data[testCount:testCount + 100]:
    checkSet.append(i)

stopWords = []
listTest = createDataSet(testSet)
listCheck = createDataSet(checkSet)
#
AllCatWords = []
""" For loop that uses the CatWords function to create a single
array that includes all the words from each category separated into
different elements. Next, a second for loop does the same with
the CatWordsCount function."""
for i in CATEGORIES:
    tempResults_1 = CatWords(i, testSet)
    AllCatWords.append(tempResults_1)
AllCatWordCounts = []
for i in AllCatWords:
    AllCatWordCounts.append(CatWordsCount(i))

"""for loop that takes the above arrays and creates a new array that has the
probability of the words being in each category. """
AllCatResults = []
for i in CATEGORIES:
    localIndex = CATEGORIES.index(i)
    tempResults_2 = compCat(AllCatWords[localIndex], AllCatWordCounts[localIndex])
    AllCatResults.append(tempResults_2)
# Array that uses the probCat function to determine prob of article
probArticleType = probCat(CATEGORIES)

""" For loop that does the calculation for determining the likelihood
of each article falling into each separate category. Ex: if there are
3 keywords it will find the probability of the article being in the
first category and multiple that by the probability of each of those
keywords being in that category. It then stores that info into an
element for that array."""
testCounter = 0
total = 0
resultsRecord = []
res = []
catRes = []
for i in AllCatResults:
    res.clear()
    for z in i:
        calcValue = probArticleType[testCounter]
        for y in z:
            calcValue = calcValue * y[1]
        res.append(calcValue)
    catRes.append(res[:])
    testCounter += 1

"""The above for loop saves probability data in this format:
[(cat1_art1prob), (cat1_art2prob), (cat1_art3prob)]
[(cat2_art1prob), (cat2_art2prob), (cat2_art3prob)]
this loop rearranges the list to be the following:
[(cat1_art1prob), (cat2_art1prob), (cat3_art1prob)]
[(cat1_art2prob), (cat2_art2prob), (cat3_art2prob)]
this allows us to compare the probabilities of a each
category for a single article."""
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

"""For loop that determines the max value in each element
this max value is the most likely category the article fall in
to based on the bayesian calculations done above"""
finalResult = []
for i in wordRes:
    finalResult.append([i.index(max(i)), max(i)])

"""Compares our answer using Bayesian formula with the correct
answer provided by the original JSON file."""
TotalTotal = 0
finalArray = [0]*29
totalFinalArray = [0]*29

for i in finalResult:
    totalFinalArray[i[0]] += 1
    if CATEGORIES[i[0]] in str(checkSet[counter]):
        TotalTotal += 1
        finalArray[i[0]] += 1
    counter += 1
print(finalArray)
print(totalFinalArray)
counter = 0
for i in finalArray:
    accuracyRound = 0
    if totalFinalArray[counter] != 0:
        accuracy = finalArray[counter]/totalFinalArray[counter]
        accuracyRound = round(accuracy, 2)*100
    print("Cat: " + str(CATEGORIES[counter]) + " " + str(accuracyRound) + "%")
    counter += 1

print(TotalTotal)
print(len(checkSet))

totalAccuracy = TotalTotal/len(checkSet)*100
totalAccuracyRound = round(totalAccuracy, 2)
print("total accuracy: " + str(totalAccuracyRound))

print(len(data))


#code here
print(f'Time taken to run: {time() - start} seconds')
