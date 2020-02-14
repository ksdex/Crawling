### Update on Feb 14, 2020 by Tianran:
1. Everything should be wrapped up now. It can ask from the running terminal whether you need to rebuild the index, and if not, you can use the previous 10-page index for testing. Then it asks for a query word, and returns the score and all links that contain that word.
2. **TODO**
- Filter out stop words in index.py
- Generate the whole index
- report


### Update on Feb 14, 2020 by Sam:
1. Write some code based on my imagination for those tasks in to-do list. I put them them in comment because I am not sure if they are all right.


### Update on Feb 13, 2020 by Tianran:
1. fix the inverted index by
- replace weird nested lists with linked lists (deque in collections)
- calcuate and append the tf-idf score to the first index of invered index as the current ranking score
2. to do
- load inverted index back to the program
- load bookkeeping.json to get the query result (it would be better if we don't need to do this though)


### One day by Sam:
Check the code and run the main function to see the process

1.You must install nltk.wordnet before you run the code
2.Make sure the WEBPAGES_CLEAN dataset is in the same dir of the .py file


Run a python script:
>>>import nltk
>>>nltk.download()

Then find the wordnet and install it.
