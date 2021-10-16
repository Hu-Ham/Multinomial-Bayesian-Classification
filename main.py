import json


data = [json.loads(line) for line in open('News_Category_Dataset_v2.json', 'r')]

counter = 0
#testCount determines what 20% of the json file is
testCount = round(.2*len(data))
#testSet is a list of the first 20% of the json file to use as test set
#checkset is a list of the remaining 80% to run through our bayesian model
testSet = []
checkSet = []

#Appends the first 20% of the json into testSet
for i in data[0:testCount]:
    testSet.append(i)
 #Appends the rest into checkSet   
for i in data[testCount+1: ]:
    checkSet.append(i)

#Prints length of each list and examples of records so we can start parsing information we need
print("There are " + str(len(testSet)) + " records in the Test set. \n First 10 are: ")
for i in testSet[0:10]:
    print(i)

print("\n\n\n\nThere are " + str(len(checkSet)) + " records in the Check set. \n First 10 are: ")
for i in checkSet[0:10]:
    print(i)
    
