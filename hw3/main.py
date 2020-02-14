import json
import time
import pathlib  
import nltk
import os
import index as partial
import datab as datab
from math import log
from collections import defaultdict, deque

def ranking_score(Index, docnum):
    tf = dict()
    for key in Index:
        print(key)
        for doc in Index[key]:
            print(doc)
            tf[key] = tf.get(key, 0) + doc[1]
    idf = dict()
    for key in Index:
        idf[key] = log(docnum) - log(len(Index[key]))
    for key in Index:
        score = tf[key] * 1.0 / idf[key]
        Index[key].appendleft(score)

def build_idx(path):
    Index = dict()
    # fileid_url_dict = partial.parse_json("WEBPAGES_CLEAN//bookkeeping.json")
    # dirs = os.listdir(path)
    dirs = ['0']
    counter = 0
    for dir in dirs:
        print('dir is:')
        print(dir)
        if os.path.isdir(path+'/'+dir):
            files = os.listdir(path+'/'+dir)
            for file in files:
                counter += 1
                with open(path+'/'+dir+'/'+file,"r",encoding="utf-8") as f1:
                    tmp_idx = datab.makeIndex(f1)
                    for key in tmp_idx:
                        if key in Index:
                            Index[key] += tmp_idx[key]
                        else:
                            Index[key] = tmp_idx[key]
                    print(path+'/'+dir+'/'+file)
                    #prints to json every 10 files
                    if counter == 10:
                        break
            ranking_score(Index, counter)
            with open("index.json", "w") as f:
                list_Index = defaultdict()
                for key in Index:
                    list_Index[key] = list(Index[key])
                x = json.dumps(list_Index)
                f.write(x)
    return Index

# suppose query is a word
def do_query(Index, q):
    # TODO: load inverted index from json
    if q in Index:
        for doc in Index[q]:
        # TODO: get result from bookkeeping.json with doc[0] as the doc_id

if __name__ == "__main__":
    path = "WEBPAGES_CLEAN"
    Index = build_idx(path)
    query = "word"
    do_query(Index, query)