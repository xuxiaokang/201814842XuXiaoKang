#对数据集进行预处理（剔除HTML标签、分词、去掉stopwords）
# _*_ coding: utf-8 _*_

import os
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def read_file(path):
    file = open(path, "rb")
    content = file.read()
    file.close()
    string=content.decode('utf-8','ignore')
    return string

def save_file(path ,content):
    file = open(path, "w")
    file.write(content)
    file.close()


#原数据集
dataPath = "D:/研一上/Data Mining/datamining/201814842XuXiaoKang/20news-18828/"
#处理完的数据集
preDataPath = "D:/研一上/Data Mining/datamining/201814842XuXiaoKang/preprocess-data/"

tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()
stopWords = set(stopwords.words('english'))

print(stopWords)

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
        content = content.lower()
        
        #用nltk先将文本拆分成句子，然后对句子进行分词
        #sentences = nltk.sent_tokenize(content)
        #words = []
        #for sentence in sentences:
        #对句子分词
        wordTokens = tokenizer.tokenize(content)
        #stemmedTokens = [stemmer.stem(token) for token in wordTokens]
        #stemmedTokens = map(stemmer.stem,wordTokens)
        
        #去掉数字和单个字符
        filteredWords = [w for w in wordTokens if not w in stopWords]
        filteredWords2 = [w for w in filteredWords if not w in ' \t1234567890abcdefghijklmnopqrstuvwxyz']
        filteredWords3 = [w for w in filteredWords2 if not str(w).isdigit()]
        #words.append(filteredWords)
        content = '\n'.join(('%s' %id for id in filteredWords3))
        #lines = filter(lambda ch:ch not in ' \t1234567890abcdefghijklmnopqrstuvwxyz',content)
        save_file(saveDir+fileName ,content)
        
print("data preprocessing finished!")