# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:48:14 2018
计算文档的TFIDF
构建字典
@author: xuxiaokang
"""

import os
import math

#读取每个文件，建立词典，并进行筛选，保留出现次数>13次的单词，写入文件中
def build_word_map():
    wordMap={}
    newWordMap={}
    #新闻数据集path
    newsDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data'
    newsFilesList = os.listdir(newsDir)
    
    for i in range(len(newsFilesList)):
        
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        newsList = os.listdir(newsFilesDir)
        
        for j in range(len(newsList)):
            fileDir = newsFilesDir+'/'+newsList[j]
            #按行读取单词，构建字典，统计单词出现次数
            for line in open(fileDir).readlines():
                word = line.strip('\n')
                wordMap[word] = wordMap.get(word,0.0)+1.0
    #筛选出出现次数大于13次的单词
    for key,value in wordMap.items():
        if value > 13:
            newWordMap[key] = value
    
    #將单词统计情况写入文件中
    #wordMapFile = open('D:/研一上/Data Mining/datamining/201814842XuXiaoKang/wordDict.txt','w')
    
    #wordCount = 0
    #for key,value in newWordMap.items():
    #    wordMapFile.write('%s %.1f\n' % (key,value))
    #    wordCount+=1
    #print('build word Map finished! size: %d' % wordCount)
    return newWordMap
#对每个文件进行筛选，保留在字典中的单词，用以计算tfidf然后构建向量
def filter_file():
    wordMap= build_word_map()
    newsDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data'
    newsFilesList = os.listdir(newsDir)
    
    for i in range(len(newsFilesList)):
        targetFileDir = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/filtered-data'+'/'+newsFilesList[i]
        newsFilesDir = newsDir+'/'+newsFilesList[i]
        if os.path.exists(targetFileDir)==False:
            os.makedirs(targetFileDir)
        newsList = os.listdir(newsFilesDir)
        for j in range(len(newsList)):
            targetFile = targetFileDir+'/'+newsList[j]
            file = open(targetFile,'w')
            fileDir = newsFilesDir+'/'+newsList[j]
            for line in open(fileDir).readlines():
                word = line.strip('\n')
                if word in wordMap.keys():
                    file.write('%s\n' %word)
            file.close()
    print('filtering data finished!')
filter_file()

        
    