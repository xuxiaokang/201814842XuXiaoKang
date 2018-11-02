# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:48:14 2018
构建字典，统计词频，筛选词频过低的单词
对每个文件进行过滤，只保留在词典中的单词
划分数据集，将数据集划分为训练集和测试集80%为训练集 20%为测试集
@author: xuxiaokang
"""

import os


#读取每个文件，建立词典，并进行筛选，保留出现次数5次的单词，写入文件中
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
    #筛选出出现次数大于5次的单词
    for key,value in wordMap.items():
        if value > 13:
            newWordMap[key] = value
    
    #將单词统计情况写入文件中
    '''
    wordMapFile = open('D:/研一上/Data Mining/datamining/201814842XuXiaoKang/wordDict.txt','w')
    
    wordCount = 0
    for key,value in newWordMap.items():
        wordMapFile.write('%s %.1f\n' % (key,value))
        wordCount+=1
    print('build word Map finished! size: %d' % wordCount)
    '''
    #返回统计情况
    return newWordMap



    
#对每个文件进行筛选，保留出现在字典中的单词，用以计算tfidf然后构建向量
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

        
    
#按80%为训练数据集，20%为测试数据集划分数据集
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
                targetFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/test-'+str(index)+'/'+newsFilesList[i]
            else:
                targetFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/partition-data/train-'+str(index)+'/'+newsFilesList[i]
            
            if os.path.exists(targetFile) == False:
                os.makedirs(targetFile)
                
            file = newsFilesDir+'/'+newsList[j]
            lines = open(file).readlines()
            targetW = open(targetFile+'/'+newsList[j],'w')
            
            for line in lines:
                targetW.write('%s\n'% line.strip('\n'))
            
            targetW.close()
    cateFile.close()
    
    
#建词典，统计词频，筛选
#build_word_map()
#对着词典过滤文件中词频过小的单词
#filter_file()
#划分数据集，执行五次 

for i in range(5):
    cateFile = 'D:/研一上/Data Mining/datamining/201814842XuXiaoKang/category'+str(i)+'.txt'
    partition_data(i,cateFile)
print('partition data finished!')
    

        
    