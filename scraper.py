import json 
import requests
from bs4 import BeautifulSoup
import requests_random_user_agent
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

company = input("Enter a company: ")
f = open("company_tickers.json")
data = json.load(f)
tickerCIK = {}
for i, l in data.items():
    currTicker = l['ticker']
    currCIK = l['cik_str']
    tickerCIK[currTicker] = currCIK
path = "/Users/anish/sentient/10Ks/"
os.chdir(path)
try:
    os.mkdir(str(tickerCIK[company]))
    os.chdir(str(tickerCIK[company]))
except OSError:
    print(company + "'s CIK has been previously utilized")


s = requests.Session()
#print(s)
url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000"+ str(tickerCIK[company]) +"&type=10-K%25&dateb=&owner=exclude&start=0&count=40&output=atom"
#print(url)
xml = requests.get(url)
soup = BeautifulSoup(xml.content, 'lxml')
tenKs = soup.find_all('filing-href')

documents = []

counter = 0
for tenK in tenKs:
    
    kurl = tenK.text
    file = requests.get(kurl)
    soup = BeautifulSoup(file.content, 'html')
    
    kurls = [i['href'] for i in soup.find_all('a', href=True)]
    docURL = "https://www.sec.gov/" + kurls[9]


    
    
    if("ex" not in docURL and "k" in docURL):
        #print(str(counter) + ": " + docURL)
        kfile = requests.get(docURL)

        if("ix?" not in docURL):
            soup = BeautifulSoup(kfile.content, 'html')
            file = company + "_" + str(counter) + ".txt"
            text = open(file, 'a')
            text.write(soup.get_text())
            text.close()
            #print(soup.get_text())
            documents.append(file)
    counter+=1

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
            , 'u', 'v', 'w', 'x', 'y', 'z']

for document in documents:
    filtered = []
    text = open(document, "r").read()
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    for word in text:
        word = word.lower()
        if(word not in stopwords.words('english') and word not in alphabet and word.isalpha()):
            word = WordNetLemmatizer().lemmatize(word)
            filtered.append(word)
    print(filtered)
    
