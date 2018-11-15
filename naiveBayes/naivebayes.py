# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:17:10 2018
朴素贝叶斯分类器
测试文档属于类的概率 = 类中出现该文档中词的概率的乘积*出现该类别的概率
@author: xuxiaokang
"""
import os
from math import log
'''
统计每个类别下的单词以及每个单词出现的次数
'''
def countWords(trainFile):
    
    newsDir = trainFile#新闻数据集路径
    newsFilesList = os.listdir(newsDir)
    wordsOfCate = {}#每个类别中的单词，以及单词出现次数
    wordsNumOfCate = {}#每个类别下单词数目
    for i in range(len(newsFilesList)):
        wordCount = 0
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        newsList = os.listdir(newsFilesDir)
        #统计每个类下单词的数目
        for j in range(len(newsList)):
            file = newsFilesDir+'/'+newsList[j]
            lines = open(file).readlines()
            #统计每个文件中单词的数目
            for line in lines:
                wordCount = wordCount+1
                word = line.strip('\n')
                wordOfCate = newsFilesList[i]+'_'+word
                wordsOfCate[wordOfCate] = wordsOfCate.get(wordOfCate,0)+1
        wordsNumOfCate[newsFilesList[i]] = wordCount
        print('%s has %d words'%(newsFilesList[i],wordCount))
    
    print('count words finished')
    return wordsOfCate,wordsNumOfCate

def computeProbability(cate,testWords,wordsNumOfCate,wordsNum,wordsOfCate):
    probability = 0
    wordsNumCate = wordsNumOfCate[cate]
    for i in range(len(testWords)):
        wordOfCate = cate+'_'+testWords[i]
        if wordOfCate in wordsOfCate:
            wordCount = wordsOfCate[wordOfCate]
        else:
            wordCount = 0.0
        prob = log((wordCount+0.00003)/(wordsNumCate+wordsNum))
        probability = probability + prob
    
    return (probability+log(wordsNumCate)-log(wordsNum))
'''
划分数据集
80%为训练集
20%为测试集
'''
def partition_data(index,category,proportion=0.8):
    
    newsDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/filtered-data'
    newsFilesList = os.listdir(newsDir)
    #记录当前文件夹中文件的分类信息
    cateFile = open(category,'w')
    for i in range(len(newsFilesList)):
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        newsList = os.listdir(newsFilesDir)
        
        l = len(newsList)
        #每次按比例划分文件
        begin = index*(l*(1-proportion))
        end = (index+1)*(l*(1-proportion))
        
        for j in range(l):
            #在区间内的是训练文件
            if (j>begin) and (j<end):
                cateFile.write('%s %s\n'%(newsList[j],newsFilesList[i]))
                targetFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/naive_bayes-data/test-'+str(index)+'/'+newsFilesList[i]
            else:
                targetFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/naive_bayes-data/train-'+str(index)+'/'+newsFilesList[i]
            
            if os.path.exists(targetFile) == False:
                os.makedirs(targetFile)
                
            file = newsFilesDir+'/'+newsList[j]
            lines = open(file).readlines()
            targetW = open(targetFile+'/'+newsList[j],'w')
            
            for line in lines:
                targetW.write('%s\n'% line.strip('\n'))
            
            targetW.close()
    cateFile.close()
    
def naiveBayes(trainFile,testFile,resultFile):
     wordsOfCate,wordsNumOfCate = countWords(trainFile)
     resultWriter = open(resultFile,'w')#记录结果
     trainWordsNum = sum(wordsNumOfCate.values())
     allCount = 0
     rightCount = 0
     newsDir = testFile
     newsFilesList = os.listdir(newsDir)
     for i in range(len(newsFilesList)):
         
         newsFilesDir = newsDir+'/'+newsFilesList[i]
         newsList = os.listdir(newsFilesDir)
         for j in range(len(newsList)):
             allCount = allCount+1
             testWords = []#统计当前测试文档的单词
             file = newsFilesDir+'/'+newsList[j]
             lines = open(file).readlines()
             for line in lines:
                 
                 word = line.strip('\n')
                 testWords.append(word)
                 
             maxProb = 0.0
             trainCate = os.listdir(trainFile)
             for k in range(len(trainCate)):
                 prob = computeProbability(trainCate[k],testWords,wordsNumOfCate,trainWordsNum,wordsOfCate)
                 
                 if k==0:
                     maxProb = prob
                     cate = trainCate[k]
                     continue
                 if prob>maxProb:
                     maxProb = prob
                     cate = trainCate[k]
                     
                    
             resultWriter.write('%s %s'%(newsFilesList[i],cate))
             if newsFilesList[i] == cate:
                 rightCount = rightCount+1
             resultWriter.write('\n')
     resultWriter.close()
     print('accuracy = %.6f'%(float(rightCount)/float(allCount)))
     return (float(rightCount)/float(allCount))
#naiveBayes()
#for i in range(5):
    #cateFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/category'+str(i)+'.txt'
    #partition_data(i,cateFile)
#print('partition data finished!')
countAcc = 0.0
for i in range(5):
    trainFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/naive_bayes/train-'+str(i)
    testFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/naive_bayes/test-'+str(i)
    resultFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/naive_bayes/result'+str(i)
    acc = naiveBayes(trainFile,testFile,resultFile)
    countAcc = countAcc + acc

print('average accuracy = %.6f'%(countAcc/float(5)))
    
     
    