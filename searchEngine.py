import string
import re  # get rid of the punctuations
import requests
import os
from urllib.request import urlopen  # request to get the html page
from bs4 import BeautifulSoup as bs  # parse html page into plain text

import hashlib  # hash url of website
from stop_words import get_stop_words
from collections import defaultdict
import shutil
# TrieNode class:
# next dictionary store the character for next node
# ref array stores the occurrence lists outside the trie
class TrieNode(object):
    def __init__(self):
        self.next = {}
        self.ref = None

        # Trie class:


class Trie(object):
    def __init__(self):
        # root object store the root entry for trie tree
        self.root = TrieNode()

    def getHash(self, string):
        '''return a unique and stable hash value from hashing the website url'''
        m = hashlib.sha1(string.encode('utf-8'))
        return m.hexdigest()


    def readOccurenceList(self, file):
        ''' read occurence list from file, and map its to <hash, website url> dictionary '''
        with open(file, 'r') as f:
            content = f.readlines()
            f.close()
        lines = [x.strip() for x in content]
        mapHashToWebsiteAndFrequency = {}
        for line in iter(lines):
            line = line.split()
            # line[0] hash, line[1] url, line[2] frequency
            mapHashToWebsiteAndFrequency[line[0]] = (line[1], line[2])
        return mapHashToWebsiteAndFrequency

    def insert(self, word, website):
        '''insert key word and website url to Trie'''
        # create a iterator
        index = self.root
        # for every single character in the word
        for c in word:
            # if can't find the a character entry for the next node
            if c not in index.next:
                # create the entry
                index.next[c] = TrieNode()
            # and move to the next entry
            index = index.next[c]
        # store the reference for the corresponding website
        index.ref = word+".txt"

    def searchOne(self, word):
        '''search a single key word'''
        word = word.lower()
        # create a iterator
        index = self.root
        # for every single character in the word
        for c in word:
            # if can't find a character entry for the next node
            if c not in index.next:
                # this means we can't find a word in the trie
                return None
            # if we can find a entry for the next node
            else:
                # move to the next node
                index = index.next[c]
        # after search is done, return the references to stored for the word
        return index.ref

    def searchManyOrOne(self, words):
        '''search a sentences Or a single word'''
        # split words into a list
        words = words.split()
        allOccurenceListsForWords = {}
        for idx in range(len(words)):
            # search occurence list file with single word
            occurenceListFileName = self.searchOne(words[idx])

            directory = os.getcwd() + "/occurenceList/"
            filename = os.path.join(directory, occurenceListFileName)
            # read <hash, website url> dictionary form occurence list file
            allOccurenceListsForWords[idx] = self.readOccurenceList(filename)

        # get intersection of each query of single words
        firtWordOccurenceList = allOccurenceListsForWords.get(0)  # get the search result of the first word in the words
        # get intersection of all queries of single words
        if not firtWordOccurenceList:
            return None
        # algorithm O(mn), where m is the the number of words of the query, n is the number of the url of the first word query
        # loop through the query list of first word
        for k, v in firtWordOccurenceList.items():  # O(m)
            # loop through other queries' list one by one
            for idx, occurenceList in allOccurenceListsForWords.items():  # O(n)
                # if not exist in other list, remove that url of the website
                if occurenceList.get(k) is None:  # O(1)
                    firtWordOccurenceList[k] = None

        res = {}
        for hashValue, websiteAndFrequencyTuple in firtWordOccurenceList.items():
            if websiteAndFrequencyTuple is not None:
                res[hashValue] = websiteAndFrequencyTuple

        return res

def getHash(url):
    '''return a unique and stable hash value from hashing the website url'''
    m = hashlib.sha1(url.encode('utf-8'))
    return m.hexdigest()

def readURLsFromFile(inputURL):
    '''return a tuple pair (key word, website url)'''
    try:
        f = open(inputURL, 'r')
        urls = f.read().split()
    except:
        print("Error while reading file: %(inputURL)s" % locals())
        return

    #get stop words with python stop_words library
    stop_words = set(get_stop_words('english'))

    # make dir to store occurence list to disk
    directory = os.getcwd() + "/occurenceList/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        # clear the the directory and sub files
        shutil.rmtree(directory)
        # make new directory
        os.makedirs(directory)

    res = []
    for idx, website in enumerate(urls):
        print('Processing website: %(website)s\n' % locals())
        # excluding stop words such as articles, prepositions, and pronouns

        # get the current page for the website url, and make them into lowercase
        try:
            page = requests.get(website)
            if page.status_code != 200:
                 raise "Invalid website"
        except:
            print('Invalid website url: %(website)s' % locals())
            print()
            continue


        # use beautifulsoup to parse the html page
        soup = bs(page.content,"html.parser")
        # get rid of the <script> tag and its content in html page
        [s.extract() for s in soup('script')]
        # get the plain text from the html page
        content = soup.get_text().strip().lower()  # content is string type
        # replace all punctuations from the plain text with space, and devide them by space
        content = re.sub(r'\n+\s*', '\n', content)

        content = re.sub(r'[0-9]+[a-zA-Z]*', ' ', content)
        content = re.sub(r'[^A-Za-z0-9]+', ' ', content).split()  # content is list type


        mapWordToFrequency = defaultdict(int)

        for word in content:
            if word not in stop_words:  # filter out stopwords
                mapWordToFrequency[word] += 1

        mapWordToWebsiteUrl = {}

        for word, frequency in mapWordToFrequency.items():
                filename = os.path.join(directory, word + ".txt")

                # create file if not exist else append string to it
                with open(filename, 'a+') as file:
                    file.write(str(getHash(website)) + " " + str(website) + " " + str(frequency) + '\n')
                    file.close()

                mapWordToWebsiteUrl[word] = website

        res.append(mapWordToWebsiteUrl)

    return res


if __name__ == '__main__':
    res = readURLsFromFile("input.txt")

    #build Trie
    trie = Trie()
    for webDict in res:
        for word, website in webDict.items():
            trie.insert(word, website)

    #search words
    with open('output.txt', 'w') as f:
        f.write('Query: time\n')
        resultList = trie.searchManyOrOne("time")
        if resultList != None:
            resultString = '\n'.join([v[0]+" "+v[1] for k, v in resultList.items()])
            f.write("Result: \n" + resultString + "\n")

        f.write('Query: python\n')
        resultList = trie.searchManyOrOne("python")
        if resultList != None:
            resultString = '\n'.join([v[0] + " " + v[1] for k, v in resultList.items()])
            f.write("Result: \n" + resultString + "\n")

        f.write('Query: python string\n')
        resultList = trie.searchManyOrOne("python string")
        if resultList != None:
            resultString = '\n'.join([v[0] + " " + v[1] for k, v in resultList.items()])
            f.write("Result: \n" + resultString + "\n")

        f.close()

    print("All Done! Please see output.txt file in the current directory.")


