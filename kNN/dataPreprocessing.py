#对数据集进行预处理（剔除HTML标签、分词、去掉stopwords）
# _*_ coding: utf-8 _*_

import os
import nltk
def read_file(path):
    file = open(path, "rb")
    content = file.read()
    file.close()
    string=content.decode('utf-8','ignore')
    return string

def save_file(path ,content):
    file = open(path, "wb")
    file.write(content)
    file.close()


#原数据集
dataPath = "D:/研一上/Data Mining/datamining/201814842XuXiaoKang/20news-18828/"
#处理完的数据集
preDataPath = "D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data/"
#stopwords文件路径
stopWordsPath = "D:/研一上/Data Mining/datamining/201814842XuXiaoKang/kNN/stopWords.txt"
file = open(stopWordsPath, "r")
lines = file.readlines()
for line in lines:
    print(line.strip())
    
    

dirList = os.listdir(dataPath)
for dirPath in dirList:
    classPath = dataPath+dirPath+"/"
    saveDir = preDataPath + dirPath + "/"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    filePathList = os.listdir(classPath)
    for fileName in filePathList:
        path = classPath+fileName
        content = read_file(path).strip()
        #用nltk先将文本拆分成句子，然后对句子进行分词
        sentences = nltk.sent_tokenize(content)
        words = []
        for sentence in sentences:
            words.append(nltk.word_tokenize(sentence))
        content = ' '.join(('%s' %id for id in words))
        #删除停用词标点符号等
        save_file(saveDir+fileName ,content)
        
print("data preprocessing finished!")