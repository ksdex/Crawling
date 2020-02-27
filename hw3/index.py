import datab
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urldefrag
from nltk.tokenize import RegexpTokenizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.corpus import stopwords
from pympler import asizeof
import json
import numpy as np
from math import log10
import sys
import re
import nltk
import os

nltk.download('stopwords')


def get_file_list(base_dir_path):
    '''
    @base_dir_path: str
    '''
    return list(base_dir_path.rglob('*.*'))


def filter_token(target_str):
    result = []
    pattern = r"^[a-z0-9]$"
    result_char = ""

    for currentChar in target_str.lower().strip():
        # Check every character
        match = re.match(pattern, currentChar)
        if match:
            result_char += currentChar
        else:
            if (result_char != ""):
                result.append(result_char)
                result_char = ""
    # Add the last token
    if (result_char != ""):
        result.append(result_char)
    return result


def parse_content(text):
    # Tokenize
    # tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    # initial_tokens = tokenizer.tokenize(text)
    initial_tokens = nltk.tokenize.word_tokenize(text)
    # token_list = []
    wordnet_lemmatizer = WordNetLemmatizer()
    # K- added STOPWORDS
    stopWords = set(stopwords.words('english'))
    token_list = [wordnet_lemmatizer.lemmatize(token) for token in initial_tokens if token not in stopWords]
    # for token in initial_tokens:
    #     if token not in stopWords:
    # if re.match(r"^[a-z0-9]*$", token):
    #     token_list.append(wordnet_lemmatizer.lemmatize(token))
    # else:
    #     for i in filter_token(token):
    #         token_list.append(wordnet_lemmatizer.lemmatize(i))

    freq_dict = FreqDist(token_list)
    # print("Finish counting frequency.")
    return freq_dict


def parse_json(json_file_path):
    json_file = None
    try:
        # print("file:", json_file_path)
        json_file = open(Path(json_file_path), "r", encoding="utf-8")
        json_dict = json.loads(json_file.read())
        return json_dict

    finally:
        if json_file != None:
            json_file.close()


def ranking_score(Index, docnum):
    # raw = list()
    for key in Index:
        print("Calculating idf for word ", key, ": ")
        idf = log10(docnum) - log10(len(Index[key]))
        print("Calculating tf-idf score for word ", key, ": ")
        for doc in Index[key]:
            doc[2] = (1.0 + log10(doc[1])) * idf
            # raw.append(doc[2])
        # print("Normalizing ...")
        # norm = 1 / np.sqrt(((np.array(raw)**2).sum()))
        # for doc in Index[key]:
        #     doc[2] = doc[2] * norm


def build_idx(path):
    Index = dict()
    # TODO: use the commented definition of dirs for final test
    dirs = os.listdir(path)
    # dirs = ['1', '2']
    counter = 0
    for dir in dirs:
        print('Current Directory:')
        print(dir)
        if os.path.isdir(path + '/' + dir):
            files = os.listdir(path + '/' + dir)
            for file in files:
                if os.path.getsize(path + '/' + dir + '/' + file) < 200000:
                    counter += 1
                    with open(path + '/' + dir + '/' + file, "r", encoding="utf-8") as f1:
                        tmp_idx = datab.makeIndex(f1)
                        for key in tmp_idx:
                            if key in Index:
                                Index[key] += tmp_idx[key]
                            else:
                                Index[key] = tmp_idx[key]
                        print(path + '/' + dir + '/' + file)
    ranking_score(Index, counter)
    print(Index)
    with open("index.json", "w") as f:
        list_Index = defaultdict()
        for key in Index:
            list_Index[key] = list(Index[key])
        x = json.dumps(list_Index)
        f.write(x)


def load_idx():
    index = json.load(open("index.json"))
    return index


def getTitleText(soup):
    title = soup.findAll('title')
    text = ""
    for titletext in title:
        text += titletext.getText()
    return text.casefold().replace("\t", "").replace("\n", " ")

def getImporText(soup):
    text = ""

    num = 1
    head = soup.findAll('h'+str(num))
    while len(head) != 0:
        for headtext in head:
            text += headtext.getText()
        num += 1
        head = soup.findAll('h' + str(num))

    bold = soup.findAll('b')
    for boldtext in bold:
        text += boldtext.getText()

    return text.casefold().replace("\t", "").replace("\n", " ")

def getBodytext(soup):
    [s.extract() for s in soup(['title', 'style', '[document]', 'head', 'meta', 'script'])]
    text = soup.getText()

    return text.casefold().replace("\t", "").replace("\n", " ")


if __name__ == "__main__":
    # build_idx("WEBPAGES_CLEAN")
    f1 = open("WEBPAGES_RAW/2/1", "r", encoding="utf-8")
    text1 = "Thành phố Irvine, liên có dân"
    counter = parse_content(text1)
    for key in counter:
        print(key)
        print(counter[key])
    # text = f1.read()
    # title = getTitleText(text)
    # result = title+"\n"+getImporText(text)[len(title):]
    # print(result)
    # title = getTitleText(text)
    # bodytext = getBodytext(text)
    # str = ""
    # while line != "":
    #     # print(line)
    #     str = str + line
    #     line = file.readline()
    #     freq_dic = partial.parse_content(str)
    # print(title)
    # print(bodytext)
