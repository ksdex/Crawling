
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
import sys
import re
import nltk
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


def parse_content(html_content, valid = True):

    if valid:
        soup = BeautifulSoup(html_content, features="html.parser")
        text = soup.get_text().lower().replace("\t", "").replace("\n", " ")
    text = re.sub(r'[^\x00-\x7F]+', " ", text)
    # Tokenize
    tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
    initial_tokens = tokenizer.tokenize(text)
    token_list = []

    #K- added STOPWORDS 
    stopWords = set(stopwords.words('english')) 


    #lancaster_stemmer = LancasterStemmer()
    wordnet_lemmatizer = WordNetLemmatizer()
    for token in initial_tokens:
        if token not in stopWords:
            if re.match(r"^[a-z0-9]*$", token):
                token_list.append(wordnet_lemmatizer.lemmatize(token))
            else:
                for i in filter_token(token):
                    token_list.append(wordnet_lemmatizer.lemmatize(i))
    freq_dict = FreqDist(token_list)
    #print("Finish counting frequency.")
    return freq_dict


def parse_json(json_file_path):

    json_file = None
    try:
        # print("file:", json_file_path)
        json_file = open(Path(json_file_path), "r", encoding = "utf-8")
        json_dict = json.loads(json_file.read())
        return json_dict

    finally:
        if json_file != None:
            json_file.close()