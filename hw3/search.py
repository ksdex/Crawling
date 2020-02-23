import json
import time
import pathlib
import nltk
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
from math import log
from collections import defaultdict, deque
import UI as ui

# suppose query is a word
def do_query(q, index, url_path):
    fileid_url_dict = partial.parse_json(url_path + "//bookkeeping.json")
    #index = partial.parse_json(index_path) removed this to load dict index in fn parameter
    print(index)
    listofid = list()
    listofurl = list()
    score = list()
    if q in index:
        # TODO: get result from bookkeeping.json with doc[0] as the doc_id
        print("index here")
        print(index[q])
        for doc in index[q]:
            if not isinstance(doc, float):
                listofid.append(doc[0])
                listofurl.append(fileid_url_dict[doc[0]])

            else:
                score.append(doc)
    print("TF-IDF score: ", score[0])
    print("number of results")
    print(len(listofurl))
    # print("Results: ")
    # for i in range(20):
    #     print(listofurl[i])
    return listofurl



