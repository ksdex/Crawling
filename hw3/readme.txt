## Update on Feb 13, 2020 by Tianran:
1. fix the inverted index by
i) replace weird nested lists with linked lists (deque in collections)
ii) calcuate and append the tf-idf score to the first index of invered index as the current ranking score
2. to do
i) load inverted index back to the program
ii) load bookkeeping.json to get the query result (it would be better if we don't need to do this though)


## One day by Sam:
Check the code and run the main function to see the process

1.You must install nltk.wordnet before you run the code
2.Make sure the WEBPAGES_CLEAN dataset is in the same dir of the .py file


Run a python script:
>>>import nltk
>>>nltk.download()

Then find the wordnet and install it.
