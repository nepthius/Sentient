from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import requests
import os
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
from gensim.models import TfidfModel
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pyLDAvis.gensim_models
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from textblob import TextBlob
import seaborn as sns
import pandas as pd
app = Flask(__name__)


@app.route("/")
def homepage():
    """View function for Home Page."""
    return render_template("index.html")


@app.route("/10k-analysis", methods=['GET', 'POST'])
def analysisPage():
    def mapTickerCIK():
        path = "/Users/anish/Sentient/"
        os.chdir(path)
        """
        Map stock tickers to CIKs.
        """
        f = open("company_tickers.json")
        data = json.load(f)
        tickerCIKs = {}
        for i, l in data.items():
            currTicker = l['ticker']
            currCIK = l['cik_str']
            tickerCIKs[currTicker] = currCIK
        return tickerCIKs

    def fetchDocuments(tickerCIKs, company):
        """
        Fetch all the documents and store them into our local folder.
        """
        path = "/Users/anish/Sentient/10Ks/"
        os.chdir(path)
        try:
            os.mkdir(str(tickerCIKs[company]))
            os.chdir(str(tickerCIKs[company]))
        except OSError:
            print(company + "'s CIK has been previously utilized")
            return
        
        s = requests.Session()
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000"+ str(tickerCIKs[company]) +"&type=10-K%25&dateb=&owner=exclude&start=0&count=40&output=atom"
        xml = requests.get(url)
        soup = BeautifulSoup(xml.content, 'html.parser')
        tenKs = soup.find_all('filing-href')

        # Fetch the documents and save into our local folder
        documentNames = [] # the filenames of all the documents
        counter = 0
        for tenK in tenKs:
            kurl = tenK.text
            file = requests.get(kurl)
            soup = BeautifulSoup(file.content, 'html.parser')
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
                    documentNames.append(fileName)
            counter += 1
        return documentNames


    def processData(documentNames):
        """
        Data cleaning + preprocessing by tokenization, removing stopwords, and lemmatization.
        """
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
                    , 'u', 'v', 'w', 'x', 'y', 'z']
        # Data cleaning + preprocessing
        dataset = []
        for documentName in documentNames:
            filtered = []
            text = open(documentName, "r").read()
            text = BeautifulSoup(text, 'html.parser').get_text() # remove HTML tags
            tokenizer = RegexpTokenizer(r'\w+')
            text = tokenizer.tokenize(text) # Tokenization
            for word in text:
                word = word.lower()
                if(word not in stopwords.words('english') and word not in alphabet and word.isalpha()): # remove stopwords
                    word = WordNetLemmatizer().lemmatize(word) # lemmatization
                    filtered.append(word)
            dataset.append(filtered)
        return dataset


    def generateBoW(dataset):
        """
        Generates the BoW of the current dataset.
        """
        dict = corpora.Dictionary(dataset)
        BoW_corpus = [dict.doc2bow(file, allow_update=True) for file in dataset]
        # id_words = [[(dict[id], count) for id, count in line] for line in BoW_corpus]
        return BoW_corpus


    def wordCloud(dataset):
        """
        Generates + displays the wordcloud of the latest report. Can be some fun feature.
        """
        wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", width=800, height=400).generate(" ".join(dataset[0]))
        plt.figure( figsize=(20,10), facecolor='k' )
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def top20(dataset):
        counter=Counter(dataset[0]) #first documents tokens from docs(which contains many tokens from different docs)
        most=counter.most_common()
        x, y=[], []
        for word,count in most[:20]:
            x.append(word)
            y.append(count)
        plt.figure(figsize=(16,6))    
        sns.barplot(x=y,y=x)

    def CosSim(A, B):
        """
        Calculate the cosine similarity between two sets A and B.
        """
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
        

    def JaccardSim(A, B):
        """
        Calculate the Jaccard similarities between two sets A and B.
        """
        return len(A.intersection(B)) / len(A.union(B))


    def computeSim(dataset):
        """
        Generate CosSim and JaccardSim for every two years, starting from the latest.
        """
        l = 0 # 0 is the latest year
        thisYearLastYear = {}
        A = set(dataset[0])
        for r in range(1, len(dataset)):
            B = set(dataset[r])
            cos_score = CosSim(A, B)
            jaccard_score = JaccardSim(A, B)
            scores = []
            scores.append(cos_score)
            scores.append(jaccard_score)
            thisYearLastYear["(" + str(l) + "-" + str(r) + ")"] = scores
            l += 1
        return thisYearLastYear


    def getPositivity(dataset):
        """
        Get the positivity of the current report.
        """
        positivity = TextBlob(" ".join(dataset[0])) # assuming for the latest 10K.
        return positivity.sentiment

    """View function for About Page."""
    if request.method == 'POST':
        """
        The driver of the program
        """
        company = request.form.get('javascript_data')
        tickerCIKs = mapTickerCIK()
        documentNames = fetchDocuments(tickerCIKs, company)
        dataset = processData(documentNames)
        thisYearLastYear = computeSim(dataset)
        #print(thisYearLastYear)
        central_df_dict = {'Pair': [], 'Cosine Similarity': [], 'Jaccard Similarity': []}
        for pair, vals in thisYearLastYear.items():
            central_df_dict['Pair'].append(pair)
            central_df_dict['Cosine Similarity'].append(vals[0])
            central_df_dict['Jaccard Similarity'].append(vals[1])
        central_df = pd.DataFrame(central_df_dict)
        central_df = central_df.set_index('Pair')
        central_df = central_df.fillna(0)
        central_df = pd.concat([central_df, central_df.pct_change()], axis=1, sort=False)
        central_df.columns = ['CosSim', 'JaccSim', 'CosSim % Change', 'Jacc % Change']
        print(central_df)
    return render_template("10k.html")


if __name__ == "__main__":
    app.run(debug=True)


