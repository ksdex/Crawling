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
from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)
import os
import index as partial
import datab as datab
from math import log
from collections import defaultdict, deque
import UI as ui
import search


def has_duplicates(d):
    return len(d) != len(set(d.values()))


if __name__ == "__main__":
    url_path = "WEBPAGES_CLEAN"
    i_build = input("Would you like to build or load the index? [B/L]")
    if i_build == 'B':
        partial.build_idx(url_path)
    index = partial.load_idx()
    # query = input("What is your query? (only word is allowed)")
    # resultlist = search.do_query(query, index, url_path)
    app = QApplication(sys.argv)
    ex = ui.SearchUI(index, url_path)
    ex.show()
    sys.exit(app.exec_())
