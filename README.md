# Simple-Search-Engine
### Install tools

First, you need to make sure you have python3 environment (preferred using virtualenv)
open the terminal in MAC OS, linux or the cmd in windows system.
Then cd to working directory, then run following commands as below:
```
pip3 install -r requirements.txt

python3 searchEngine.py
```

#### 1. input.txt:
The input.txt contains 7 website links which I used as the input source. If you want test other pages, just copy the URLs and add it to this input file. Run searchEngine.py again to update the Trie. Then you can search the keyword of those pages by adding some code in the searchEngine.py file.

#### 2. output.txt:
The output file contains the result of sample queries, which is already created by running searchEngine.py file. Feel free to run the searchEngine.py file again to recreate it.

#### 3. searchEngine.py:
This is the main program in my project.

I imported a package named beautifulsoup which is aim to parse the content of URLs in input.txt to plain text.

There are 4 parts in this file:
#### class TrieNode(object)

A compressed trie for the set of index terms, where each external node stores the index of occurrence list of the associated term.
because of their large total size, the occurrence lists are stored on disk as files in the `occurenceList` folder after running this program.

#### class Trie(object)
Search the given word in the URLs content which has already been filtered.
insert(): insert key word and website url to Trie
searchOne(): search a single key word
searchManyOrOne(): search a sentences Or a single word

#### readURLsFromFile (inputURL):
Get the website URLs then parse them to be plain text. Then do a series of data processing, like convert to lowercase, get rid of stop words, divide the plain text to multitude of single words. Then store these words and url into inverted file. After these preparation, the content is ready to be searched.

#### getHash(url):
take an url and convert it into hash value, preparing for making a dictionary for fast intersection algorithm.

### other directory and files
#### 1. occurenceList
This is a folder where I store occurence list for each word as required.

#### 2. requirements.txt
This file specify all the python3 libraries needed for this search engine project.
