# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 08:48:14 2018
计算文档的TFIDF
@author: xuxiaokang
"""

import os
import math


#计算包含Word的文档数目
def word_count_in_file(word,wordlist):
    count=0
    for i in wordlist:
        for j in i:
            if word in set(j):
                count = count+1
            else:
                continue
    return count

