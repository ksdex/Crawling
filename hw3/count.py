import json
from main import load_idx
import os

index = load_idx()
print(len(index))
# doclist = list()
# for key in index:
#     for doc in index[key]:
#         if not isinstance(doc, float):
#             doclist.append(doc[0])
# print(len(set(doclist)))

# path= "WEBPAGES_CLEAN"
# dirs = os.listdir(path)
# counter = 0
# for dir in dirs:
#     print('Current Directory:')
#     print(dir)
#     if os.path.isdir(path + '/' + dir):
#         files = os.listdir(path + '/' + dir)
#         for file in files:
#             if os.path.getsize(path + '/' + dir + '/' + file) < 10000:
#                 counter += 1
# print(counter)

