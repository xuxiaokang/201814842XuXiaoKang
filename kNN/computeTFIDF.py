# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:06:25 2018
先根据整个文件夹计算每个单词的idf值并保存
然后在文件内计算单词的tf值与idf值相乘
@author: xuxiaokang
"""

import os
from math import log

#计算idf
def computeIDF():
    newsDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data'
   
    wordMap={} #记录出现某个单词的doc
    wordIdfMap={}

    docNum = 0#统计文档总数目
    wordDocNum = 0#统计出现某个单词的文档数目
    newsFilesList = os.listdir(newsDir)
    
    #统计每个单词出现的文档
    for i in range(len(newsFilesList)):
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        newsList = os.listdir(newsFilesDir)
        
        for j in range(len(newsList)):
            file = newsFilesDir+'/'+newsList[j]
            docNum+=1
            lines = open(file).readlines()
            for line in lines:
                word = line.strip('\n')
                #用集合存储出现该单词的文档，不会重复
                if word in wordMap.keys():
                    wordMap[word].add(newsList[j])
                else:
                    wordMap.setdefault(word,set())
                    wordMap[word].add(newsList[j])
    #保存idf值               
    wordIdfFile = open('D:/研一上/Data Mining/datamining/201814842XuXiaoKang/wordIdf.txt','w')
    for word in wordMap.keys():
        wordDocNum = len(wordMap[word])
        idf = log(docNum/(wordDocNum+1))/log(10)
        wordIdfMap[word] = idf
        wordIdfFile.write('%s %.6f\n' %(word,idf))
    
    wordIdfFile.close()
    print('word IDF finished!')
    return wordIdfMap


#根据划分好的数据集，计算tfidf值，并保存
def computeTFIDF():
    #获取idf值
    wordIdfMap = computeIDF()
    
    newsDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data'
    trainFileDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/train-0/trainTfIdf.txt'
    testFileDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/test-0/testTfIdf.txt'
    
    trainWriter = open(trainFileDir,'w')
    testWriter = open(testFileDir,'w')
    
    newsFilesList = os.listdir(newsDir)
    for i in range(len(newsFilesList)):
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        newsList = os.listdir(newsFilesDir)
        
        begin = 0
        end = len(newsList)*0.2
        
        for j in range(len(newsList)):
            wordTfMap = {}
            wordOfDoc = 0
            file = newsFilesDir+'/'+newsList[j]
            lines = open(file).readlines()
            #统计tf
            for line in lines:
                wordOfDoc+=1
                word = line.strip('\n')
                wordTfMap[word] = wordTfMap.get(word,0)+1
                
            if (j>begin) and (j<end):
                writer = testWriter
            else:
                writer = trainWriter
            #将训练集和测试集每个文档的类别 文档名写入文件
            #【类别 文档名 单词 tfidf】
            writer.write('%s %s '%(newsFilesList[i],newsList[j]))
            #计算每个单词的tf*idf值
            for word,num in wordTfMap.items():
                tf = float(num)/float(wordOfDoc)
                writer.write('%s %f '%(word,tf*float(wordIdfMap[word])))
            
            writer.write('\n')
    
    trainWriter.close()
    testWriter.close()
#计算idf
#computeIDF()
#计算训练集和测试集的单词的tfidf并保存
computeTFIDF()
    
