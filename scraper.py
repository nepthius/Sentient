import json 
import requests
from bs4 import BeautifulSoup
import requests_random_user_agent
import os

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
url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000"+ str(tickerCIK[company]) +"&type=10-K%25&dateb=&owner=exclude&start=0&count=40&output=atom"
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
        kfile = requests.get(docURL)

        if("ix?" not in docURL):
            soup = BeautifulSoup(kfile.content, 'html')
            file = company + "_" + str(counter) + ".txt"
            text = open(file, 'a')
            text.write(soup.get_text())
            text.close()
            documents.append(docURL)
    
    
    counter+=1
