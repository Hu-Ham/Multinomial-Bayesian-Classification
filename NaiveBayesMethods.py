import json
import random
import math

def mean(vals):
    return sum(vals)/float(len(vals))

def stdev(nums):
    avg = mean(vals)
    vari = sum([pow(x-avg,2) for x in vals])/float(len(vals)-1)
    return math.sqrt(vari)

def calprob(x, mean, stdev):
    exp = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exp

def classprob(sumar, vec):
    probs = {}
    for classValue, classSumms in summaries.iteritems():
        probs[classValue] = 1
        for i in range(len(classSumms)):
            mean, stdev = classSumms[i]
            x = vec[i]
            probs[classValue] *= calprob(x, mean, stdev)
    return probs

def predict(summs, vec):
    probits = classprob(summs, vec)
    bestLabel, bestProb = None, -1
    for classValue, prob in probits.iteritems():
        if bestLabel is None or prob > bestProb:
            bestProb = prob
            bestLabel = classValue
    return bestLabel

def getPredictions(summs, tests):
    predicts = []
    for i in range(len(tests)):
        results = predict(summs, tests[i])
        predicts.append(results)
    return predictions

def getAccuracy(tests, predicts):
    corr = 0
    for i in range(len(tests)):
        if tests[i][-1] == predicts[i]:
            corr += 1
    return (corr/float(len(tests))) * 100.0
