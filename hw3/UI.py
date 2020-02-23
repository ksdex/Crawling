import sys
import re
import bs4
import urllib.request  
from bs4 import BeautifulSoup 
import urllib.parse
import search
from PyQt5.QtCore import QStringListModel,Qt
from PyQt5.QtGui import QPalette,QFont
from PyQt5.QtWidgets import (QListView,QPushButton,QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout,QApplication)

class SearchUI(QWidget):
    def __init__(self,index,url_path): # 初始化
        super().__init__()
        self.initUI()
        self.index = index
        self.url_path = url_path
        self.result = list()

    def initUI(self):
        search_label = QLabel("Geegle")
        search_label.setAlignment(Qt.AlignCenter)
        search_label.setFont(QFont("Roman times", 10, QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        search_label.setPalette(pe)
        search_item = QLineEdit()
        btn1 = QPushButton("Search Start!", self)
        btn2 = QPushButton("Clear", self)
        search_result = QListView()
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(search_label, 1, 0)
        grid.addWidget(search_item,2, 0)
        grid.addWidget(btn1, 3, 0)
        grid.addWidget(btn2, 3, 1)
        grid.addWidget(search_result, 4, 0, 5, 0)
        self.setLayout(grid)

        def searching():
            self.result = search.do_query(search_item.text(),self.index,self.url_path)
            slm = QStringListModel();
            slm.setStringList(self.result)
            search_result.setModel(slm)
        btn1.clicked.connect(searching)

        def clear():
            search_result.setText("")
            search_item.setText("")
        btn2.clicked.connect(clear)

        self.setGeometry(400, 150, 600, 500)
        self.setWindowTitle("Search Engine")
