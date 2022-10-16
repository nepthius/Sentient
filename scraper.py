from cmath import cos
import json 
import requests
from bs4 import BeautifulSoup
import requests_random_user_agent
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('omw-1.4')
from gensim import corpora
from gensim.models import LdaMulticore
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pyLDAvis.gensim_models
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


company = input("Enter a company: ")
f = open("company_tickers.json")
data = json.load(f)
tickerCIK = {}
for i, l in data.items():
    currTicker = l['ticker']
    currCIK = l['cik_str']
    tickerCIK[currTicker] = currCIK
path = "/Users/ducnguyen/Sentient/10Ks/"
os.chdir(path)
try:
    os.mkdir(str(tickerCIK[company]))
    os.chdir(str(tickerCIK[company]))
except OSError:
    print(company + "'s CIK has been previously utilized")


s = requests.Session()
url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000"+ str(tickerCIK[company]) +"&type=10-K%25&dateb=&owner=exclude&start=0&count=40&output=atom"
#print(url)
xml = requests.get(url)
soup = BeautifulSoup(xml.content, 'html')
tenKs = soup.find_all('filing-href')

# Fetch the documents and save into our local folder
documents = [] # the filenames of all the documents
counter = 0
for tenK in tenKs:
    
    kurl = tenK.text
    file = requests.get(kurl)
    soup = BeautifulSoup(file.content, 'html')
    
    kurls = [i['href'] for i in soup.find_all('a', href=True)]
    docURL = "https://www.sec.gov/" + kurls[9]

    
    if("ex" not in docURL and "k" in docURL):
        kfile = requests.get(docURL)

        if("ix?" not in docURL):
            soup = BeautifulSoup(kfile.content, 'html')
            text = soup.get_text()
            fileName = company + "_" + str(counter) + ".txt"
            file = open(fileName, 'a')
            file.write(text)
            file.close()
            documents.append(fileName)
    counter+=1

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
            , 'u', 'v', 'w', 'x', 'y', 'z']

# Data preprocessing + cleaning
dataset = []
for document in documents:
    filtered = []
    text = open(document, "r").read()
    text = BeautifulSoup(text, 'html.parser').get_text() # remove HTML tags
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text) # Tokenization
    for word in text:
        word = word.lower()
        if(word not in stopwords.words('english') and word not in alphabet and word.isalpha()): # remove stopwords
            word = WordNetLemmatizer().lemmatize(word) # lemmatization
            filtered.append(word)
    dataset.append(filtered)

# Generate the BoW
dict = corpora.Dictionary(dataset)
BoW_corpus = [dict.doc2bow(file, allow_update=True) for file in dataset]
id_words = [[(dict[id], count) for id, count in line] for line in BoW_corpus]

# # Display the Word Cloud
# wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", width=800, height=400).generate(" ".join(dataset[0])) #first documents tokens from docs(which contains many tokens from different docs)
# plt.figure( figsize=(20,10), facecolor='k' )
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

def CosSimilarity(A, B):
    vec_A = []
    vec_B = []
    rvector = list(A.union(B))
    for w in rvector:
        if w in A:
            vec_A.append(1)
        elif w not in A:
            vec_A.append(0)
        if w in B:
            vec_B.append(1)
        elif w not in B:
            vec_B.append(0)
    mul = 0
    for i in range(len(rvector)):
        mul += vec_A[i] * vec_B[i]
    return mul / float((sum(vec_A) * sum(vec_B)) ** 0.5)
    
def JaccardSimilarity(A, B):
    return len(A.intersection(B)) / len(A.union(B))

l = 0 # 0 is the latest year
thisYearLastYear = {}
A = set(dataset[0])
for r in range(1, len(dataset)):
    B = set(dataset[r])
    cos_score = CosSimilarity(A, B)
    jaccard_score = JaccardSimilarity(A, B)
    scores = []
    scores.append(cos_score)
    scores.append(jaccard_score)
    thisYearLastYear["(" + str(l) + "-" + str(r) + ")"] = scores
    l += 1
print(thisYearLastYear)