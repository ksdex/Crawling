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
    # TODO: use the commented definition of dirs for final test
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
            ranking_score(Index, counter)
            with open("index.json", "w") as f:
                list_Index = defaultdict()
                for key in Index:
                    list_Index[key] = list(Index[key])
                x = json.dumps(list_Index)
                f.write(x)

# suppose query is a word
def do_query(q, index_path, url_path):
    fileid_url_dict = partial.parse_json(url_path + "//bookkeeping.json")
    index = partial.parse_json(index_path)
    print(index)
    listofid = list()
    listofurl = list()
    score = list()
    if q in index:
        # TODO: get result from bookkeeping.json with doc[0] as the doc_id
        for doc in index[q]:
            if not isinstance(doc, float):
                listofid.append(doc[0])
                for id in listofid:
                    listofurl.append(fileid_url_dict[id])
            else:
                score.append(doc)
    print("TF-IDF score: ", score[0])
    print("Results: ")
    for url in listofurl:
        print(url, '\n')

if __name__ == "__main__":
    url_path = "WEBPAGES_CLEAN"
    index_path = "index.json"
    i_build = input("Would you like to build the index? [Y/N]")
    if i_build == 'Y':
        build_idx(url_path)
    query = input("What is your query? (only word is allowed)")
    do_query(query, index_path, url_path)