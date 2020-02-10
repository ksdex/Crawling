import time
from pathlib import Path

import os
import index as partial
#####
def main():
    fileid_url_dict = partial.parse_json("WEBPAGES_CLEAN//bookkeeping.json")
    path = "WEBPAGES_CLEAN"
    path2 = "WEBPAGES_CLEAN/0/2"
    dirs = os.listdir(path)
    # for dir in dirs:
    #     #print(dir)
    #     if os.path.isdir(path+'/'+dir):
    #         files = os.listdir(path+'/'+dir)
    #         for file in files:
    #             print(path+'/'+dir+'/'+file)

    file = open(path2, "r", encoding="utf-8")
    line = file.readline()
    str = ""
    while line != "":
        #print(line)
        str = str + line
        line = file.readline()
    freq_dic = partial.parse_content(str)
    for key in freq_dic:
        print(key)
        print(freq_dic[key])





if __name__ == "__main__":
    main()