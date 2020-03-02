import json
import time
import pathlib
import nltk
import numpy as np
from scipy import spatial
import sys
import re
import bs4
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from PyQt5.QtWidgets import (QPushButton,QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout,QApplication)
import os
import index as partial
import datab as datab
from math import log10
from collections import defaultdict, deque
import UI as ui
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# suppose query is a word
def do_query(q, index, url_path):
    fileid_url_dict = partial.parse_json(url_path + "//bookkeeping.json")
    #index = partial.parse_json(index_path) removed this to load dict index in fn parameter
    # print(index)
    anchor_words = ["faculty","course","community","wiki","about"]
    listofurl = list()
    score = dict()
    query = re.sub(r'[^\x00-\x7F]+', " ", q)
    query = [query.casefold() for query in nltk.tokenize.word_tokenize(query)]
    wordnet_lemmatizer = WordNetLemmatizer()
    stopWords = set(stopwords.words('english'))
    query_list = [wordnet_lemmatizer.lemmatize(token) for token in query if token not in stopWords]
    term_list = [word for word in query_list if word in index]
    term_set = set(term_list)
    freq_q = nltk.FreqDist(term_list)
    q_vec = np.zeros(len(term_set))
    for idx, word in enumerate(term_set):
        q_vec[idx] = (1.0 + log10(freq_q[word])) * (index[word][0][2] / (1.0 + log10(index[word][0][1])))
    q_vec /= np.linalg.norm(q_vec)

    # subset_index = dict(zip(list(term_set), [index[term][0] for term in term_set]))
    for term in term_list:
        for doc in index[term]:
            flag = False
            url_anchor = fileid_url_dict[doc[0]];
            for word in anchor_words:
                if word in url_anchor:
                    flag = True
            if doc[3] != 0:
                score[doc[0]] = score.get(doc[0], 0) + doc[2] + doc[3]
            else:
                score[doc[0]] = score.get(doc[0], 0) + doc[2]
            if flag:
                score[doc[0]] += 1

    for doc_id in score:
        d_vec = np.zeros(len(term_set))
        for idx, term in enumerate(term_set):
            for doc in index[term]:
                if doc_id in doc:
                    d_vec[idx] = doc[2]
                    break
        d_vec /= np.linalg.norm(d_vec)
        cos = 1 - spatial.distance.cosine(q_vec, d_vec)
        score[doc_id] += cos

    if len(score) >= 20:
        result = Counter(score).most_common(20)
        for doc in result:
            f1 = open("WEBPAGES_RAW/" + str(doc[0]), "r", encoding="utf-8")
            html_content = f1.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            print(doc[0])
            title = partial.getTitleText(soup)
            body = partial.getBodytext(soup)
            if len(body) > 120:
                resulttext = fileid_url_dict[doc[0]] + "\n" + title + "\n" + body[:120]
            else:
                resulttext = fileid_url_dict[doc[0]] + "\n" + title + "\n" + body
            listofurl.append(resulttext)
    else:
        for doc in sorted(score, key=score.get, reverse=True):
            f1 = open("WEBPAGES_RAW/" + str(doc[0]), "r", encoding="utf-8")
            html_content = f1.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            title = partial.getTitleText(soup)
            body = partial.getBodytext(soup)
            if len(body) > 20:
                resulttext = fileid_url_dict[doc[0]] + "\n" + title + "\n" + body[:20]
            else:
                resulttext = fileid_url_dict[doc[0]] + "\n" + title + "\n" + body
            listofurl.append(resulttext)
    # print("TF-IDF score: ", score[0])
    # print("number of results")
    # print(len(listofurl))
    # print("Results: ")
    # for i in range(20):
    #     print(listofurl[i])
    return listofurl



