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
        for doc in Index[key]:
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
    dirs = os.listdir(path)
    # dirs = ['1', '2']
    counter = 0
    for dir in dirs:
        print('Current Directory:')
        print(dir)
        if os.path.isdir(path+'/'+dir):
            files = os.listdir(path+'/'+dir)
            for file in files:
                if os.path.getsize(path+'/'+dir+'/'+file) < 20000:
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

def has_duplicates(d):
    return len(d) != len(set(d.values()))

# suppose query is a word
def do_query(q, index, url_path):
    fileid_url_dict = partial.parse_json(url_path + "//bookkeeping.json")
    print(has_duplicates(fileid_url_dict))
    #index = partial.parse_json(index_path) removed this to load dict index in fn parameter
    print(index)
    listofid = list()
    listofurl = list()
    score = list()
    if q in index:
        # TODO: get result from bookkeeping.json with doc[0] as the doc_id
        for doc in index[q]:
            if not isinstance(doc, float):
                listofid.append(doc[0])
                listofurl.append(fileid_url_dict[doc[0]])

            else:
                score.append(doc)
    print("TF-IDF score: ", score[0])
    print("number of results")
    print(len(listofurl))
    print("Results: ")
    for i in range(20):
        print(listofurl[i])
    return listofurl


def load_idx():
    index = json.load(open("index.json"))
    return index


if __name__ == "__main__":
    url_path = "WEBPAGES_CLEAN"
    i_build = input("Would you like to build or load the index? [B/L]")
    if i_build == 'B':
        build_idx(url_path)
    index = load_idx()
    query = input("What is your query? (only word is allowed)")
    resultlist = do_query(query, index, url_path)

