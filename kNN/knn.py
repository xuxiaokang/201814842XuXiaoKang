# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:54:49 2018
knn
@author: xuxiaokang
"""

from numpy import linalg
from numpy import mat
import operator

#计算训练向量和测试向量之间的相似性，用余弦值表示
def compute_similarity(trainData,testData):
    train = []
    test = [] 
    
    for word,tfidf in testData.items():
        if trainData.__contains__(word):
            train.append(float(trainData[word]))
            test.append(float(tfidf))
    
    trainV = mat(train)
    testV = mat(test)
    
    consin = float(testV*trainV.T) / (1.0+float(linalg.norm(testV)*linalg.norm(trainV)))
    
    return consin
#寻找k个邻居，计算分类
def classify(k,cate,test,trainMap):
    simMap = {}
    for item in trainMap.items():
        sim = compute_similarity(item[1],test)
        simMap[item[0]] = sim
    
    sortedSimMap = sorted(simMap.items(),key=operator.itemgetter(1),reverse=True)
    
    cateSimMap = {}
    for i in range(k):
        cate = sortedSimMap[i][0].split('_')[0]
        cateSimMap[cate] = cateSimMap.get(cate,0)+sortedSimMap[i][1]
    sortedCateSimMap = sorted(cateSimMap.items(),key=operator.itemgetter(1),reverse=True)
    return sortedCateSimMap[0][0]


def test():
    trainFiles = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/train-0/trainTfIdf.txt'
    testFiles = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/test-0/testTfIdf.txt'
    resultFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/test-0/result.txt'
    
    trainWordMap = {}
    
    lines = open(trainFiles).readlines()
    for line in lines:
        trainDoc = line.strip('\n').split(' ')
        trainTfIdf = {}
        l = len(trainDoc)-1
        for i in range(2,l,2):
            #取出tfidf值
            trainTfIdf[trainDoc[i]] = trainDoc[i+1]
        
        category = trainDoc[0]+'_'+trainDoc[1]
        trainWordMap[category] = trainTfIdf
    
    testWordMap = {}
    lines = open(testFiles).readlines()
    for line in lines:
        testDoc = line.strip('\n').split(' ')
        testTfIdf = {}
        l = len(testDoc)-1
        for i in range(2,l,2):
            testTfIdf[testDoc[i]] = testDoc[i+1]
        
        category = testDoc[0]+'_'+testDoc[1]
        testWordMap[category] = testTfIdf
    
    num = 0
    right = 0
    resultWriter = open(resultFile,'w')
    for item in testWordMap.items():
        #k=7
        predictClass = classify(15,item[0],item[1],trainWordMap)
        num+=1
        originalClass = item[0].split('_')[0]
        resultWriter.write('%s %s\n'%(originalClass,predictClass))
        if originalClass == predictClass:
            right += 1
        
    accuracy = float(right)/float(num)
    print('accuracy %.6f' % accuracy)
test()

    
