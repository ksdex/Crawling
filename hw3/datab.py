#import mysql.connector
import json
import time
import pathlib  
import nltk
import os
import index as partial
from collections import deque
from math import log10
from bs4 import BeautifulSoup

"""
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE index")

addToIndex(tokenList){

  for every item in tokenList {
    myDictIndex.
  }

#database should:
# token |  docID

"""

#myDictIndex = {}
#f = open("dict.json","w")


def makeIndex(file):

    titleDic = {}
    # line = file.readline()
    # str = ""
    # while line != "":
    #     #print(line)
    #     str = str + line
    #     line = file.readline()
    #     freq_dic = partial.parse_content(str)

    '''
    Sam: I change sth from here
    '''
    docID = getDocID(file)
    myDictIndex = {}
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find('title').string
    titleDic[docID] = title  # this is what I will use in UI for get title, ignore it now
    title = title.lower().replace("\t", "").replace("\n", " ")
    [s.extract() for s in soup(['title', 'style', '[document]', 'head', 'meta', 'script'])]
    body = soup.getText().lower().replace("\t", "").replace("\n", " ")

    freq_dic = partial.parse_content(body)  # not sure if it is all right for u

    '''
    change over
    '''

    #total = getWordCount(freq_dic)
    for word in freq_dic:
        #docID = getDocID(file)
        keyInfo = deque()
        # create an entry of key term in index
        keyInfo.append([docID, freq_dic[word], 0])
        # add a value of (docID, freq) to key's linkedlist
        myDictIndex[word] = keyInfo
    return myDictIndex
    

def getDocID(file):
  filePath = file.name
  docID = filePath[15:]
  return docID

"""
def getNumTerms(freq_dic):
  numterms = 0
  for term in freq_dic:
    numterms += freq_dic[term]
  return numterms

def getTF(freq,numterms):
  return freq / numterms

def getIDF(totalIndex,word):
  f = open("docCount.txt","r")
  numDocs = f.read()
  idf = numDocs / totalIndex[word].len()
  return idf


def getTFIDF(tf,idf):
  tf = freq / totalword
  tfidf = tf * math.log(idf)
  return tfidf

#adds dict to json
json = json.dumps(myDictIndex, sort_keys=True)
f.write(json)
f.close()
"""