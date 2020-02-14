import json
import time
import pathlib  
import nltk
import os
import index as partial
import datab as datab


def main():


    myIndex = {}

    fileid_url_dict = partial.parse_json("WEBPAGES_CLEAN//bookkeeping.json")
    path = "WEBPAGES_CLEAN"
    path2 = "WEBPAGES_CLEAN/0/2"
    path3 ="WEBPAGES_CLEAN/0/3"
    dirs = os.listdir(path)
    counter = 0
    for dir in dirs:
         print('dir is:')
         print(dir)
         if os.path.isdir(path+'/'+dir):
             files = os.listdir(path+'/'+dir)
             for file in files:
                 counter += 1
                 #myIndex = {}
                 #myIndex = datab.addToIndex(file)
                 f = open(path+'/'+dir+'/'+file,"r",encoding="utf-8")
                 thisIndex = datab.makeIndex(f)
                 myIndex = mergeDict(thisIndex,myIndex)
                 print(path+'/'+dir+'/'+file)
                 #prints to json every 10 files
                 if(counter % 10 == 0):
                     f = open("index.json","w")
                     x = json.dumps(myIndex)
                     f.write(x)


    #file = open(path2, "r", encoding="utf-8")
    #file2 = open(path3,"r", encoding="utf-8")


    """
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

    f = open("dict.json","w")
    json = json.dumps(myDictIndex)
    f.write(json)
    f.close()
    """

    #index for file
    #myDictIndex = datab.addToIndex(file)
    #print("first index:")
    #print(myDictIndex)
   # myDictIndex2 =datab.addToIndex(file2)
  #  print("second index:")
  #  print(myDictIndex2)


  #  myDictIndex3 = mergeDict(myDictIndex,myDictIndex2)
  #  print("merged index:")
  #  print(myDictIndex3)

    
    f.close()
    print(myIndex)
   
def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key]=(value, dict1[key])
 
   return dict3





if __name__ == "__main__":
    main()