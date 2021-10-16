import json


data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

counter = 0
testCount = round(.2*len(data))

testSet = []
checkSet = []

for i in data[0:testCount]:
    testSet.append(i)
    
for i in data[testCount+1: ]:
    checkSet.append(i)

##print("There are " + str(len(testSet)) + " records in the Test set. \n First 10 are: ")
##for i in testSet[0:10]:
##    print(i)

#print(testSet[0])
Categories = []
URLs = []
temp = ''
tempList = []
  
for i in testSet:
    temp = str(i)
    tempList = temp.split(',')
    URLs.append(tempList[3])
    if tempList[0] not in Categories:
        Categories.append(tempList[0])


def parsingString(string, delim):
    return string.partition(delim)[2]

print("Categories:")
for i in Categories:
    temp = parsingString(str(i), "'category': ")
    print(temp)
print("URLs: ")
for i in URLs[0:100]:
    temp = parsingString(str(i), "'link': ")
    print(temp)
