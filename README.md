# Simple-Search-Engine
### Approach
1. Read websites urls from `input.txt` file.
2. Crawling website contents and store the occurence list of each word in `occurrenceList` folder where the `file name` is reference for index terms and file content is the occurence list for word. The occurrence list store website url hash value, website url, word count.
3. Build compressed trie from website contents and get rid of stop words and store `file name` as reference for index terms in the external node of the trie.
4. The query for a single word takes O(n) time, where n is the length of the word. And the query from trie for sentence takes O(n) time, where n is the length of sentence. And get the intersection of all query urls takes O(nm) time, where n is the size of urls query from the first word, m is the number of words in the sentence.
5. For ranking algorithm, first we have a list of urls. For each urls we have word frequency and then sort them according the frequency in descending order. Return the sorted urls.
##### for more detailed implementation, please see python `searchEngine.py` file
### Install tools
First, you need to make sure you have python3 environment (preferred using virtualenv)
open the terminal in MAC OS, linux or the cmd in windows system.
Then cd to working directory, then run following commands as below:
```
pip3 install -r requirements.txt

python3 searchEngine.py
```

#### Files

#### 1. input.txt:
The input.txt contains 7 website links which I used as the input source. If you want test other pages, just copy the URLs and add it to this input file. Run searchEngine.py again to update the Trie. Then you can search the keyword of those pages by adding some code in the searchEngine.py file.

#### 2. output.txt:
The output file contains the result of sample queries, which is already created by running searchEngine.py file. Feel free to run the searchEngine.py file again to recreate it.
This file contains urls returned by query result and ranking them by frequency of each words. It means that the website contains more words would rank higher.
![alt text](https://github.com/HoweZZH/Simple-Search-Engine/blob/master/pictures/output.png? "original picture")

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

The search method would return urls that contains all the input words and ranking them by frequency.

#### readURLsFromFile (inputURL)
Get the website URLs then parse them to be plain text. Then do a series of data processing, like convert to lowercase, get rid of stop words, divide the plain text to multitude of single words. Then store these words and url into inverted file. After these preparation, the content is ready to be searched.

#### getHash(url)
take an url and convert it into hash value, preparing for making a dictionary for fast intersection algorithm.

### other directory and files
#### 1. occurenceList
This is a folder where I store occurence list for each word as required.
the occurenceList folder storing the occurrence list for each word.
<img src="https://github.com/HoweZZH/Simple-Search-Engine/blob/master/pictures/Picture1.png" alt="Drawing" style="width: 200px;"/>
for example,
the ‘python.txt’ file as below, there are 6 websites contain the python word.
The first line: the 1st string value is hash value calculated from the url; the 2nd string is the website url; the 3rd is the frequency of ‘python’ word in the website.
![alt text](https://github.com/HoweZZH/Simple-Search-Engine/blob/master/pictures/Picture2.png? "original picture")

#### 2. requirements.txt
This file specify all the python3 libraries needed for this search engine project.
