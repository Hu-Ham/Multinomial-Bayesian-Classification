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
import nltk 
from nltk.tokenize import word_tokenize

# Use of the NLTK package to "clean" data by removing stop-words, and then assess most common remaining words
nltk.download(['stopwords', 'punkt'])
ENGLISH_RE = re.compile(r'[a-z]+')
stop_words = nltk.corpus.stopwords.words("english")
stop_words.append('said')  # Removal of the word "said", a common stop-word not in the stop word corpus


#Importing in the json file that contains the data
data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

"""
These variables are use to cut the data set into 2 parts. The test data set is 20%
of the total dataset and will be used as reference. The checkset data set will be
80% of the original dataset and will have the bayesian calculation run on it to
determine each classification. The for loop will append each data element into a
list.
"""
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
              'EDUCATION', 'COLLEGE', 'PARENTS', 'ARTS & CULTURE', 'STYLE', 'GREEN', 'TASTE',
              'HEALTHY LIVING', 'THE WORLDPOST', 'GOOD NEWS', 'FIFTY', 'ARTS']
#List and variables needed to strip unnecessary information and tokenize each data element
headline = []
description = []
temp = ''
tempList = []
totalKeywords = []
counter = 0
tokenKeywords = []

"""
This for loop strips out the information that is not the headline or short description part
of each data element and stores them in two separate lists. The next for loop concatenates
those two lists into one. And finally the third loop strips non-alphanumeric characters except
for spaces and then tokenizes the data element.
"""
for i in testSet:
    temp = str(i)
    tempList = temp.split("'headline':")
    temp = str(tempList[1])
    tempList = temp.split("'authors'")
    headline.append(tempList[0])
    tempList = temp.split("'short_description':")
    temp = str(tempList[1])
    tempList = temp.split("'date':")
    description.append(tempList[0])

for i in range(0, len(testSet)):
    totalKeywords.append(str(description[counter]) + str(headline[counter]))
    counter += 1 

for i in totalKeywords:
    s = re.sub(r'[^A-Za-z0-9 ]+', '', i)
    tokenKeywords.append(word_tokenize(s))

for i in tokenKeywords:
    print(i)
     

