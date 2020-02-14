#import mysql.connector
import json
import time
import pathlib  
import nltk
import os
import index as partial

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
  myDictIndex = {}
  line = file.readline()
  str = ""
  while line != "":
    #print(line)
    str = str + line
    line = file.readline()
    freq_dic = partial.parse_content(str)
      
  #total = getWordCount(freq_dic)
  for word in freq_dic:
    TFIDF = 0
    docID = getDocID(file)
    # create an entry of key term in index
    freq = freq_dic[word] 
    keyInfo = [docID,freq,TFIDF]
    # add a value of (docID, freq) to key's linkedlist
    myDictIndex[word] = (keyInfo)
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