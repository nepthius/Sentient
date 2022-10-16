import json 
import requests
from bs4 import BeautifulSoup
import requests_random_user_agent

company = input("Enter a company: ")
f = open("company_tickers.json")
data = json.load(f)
tickerCIK = {}
for i, l in data.items():
    currTicker = l['ticker']
    currCIK = l['cik_str']
    tickerCIK[currTicker] = currCIK
tickerCIK[company] 


s = requests.Session()
#print(s)
url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000"+ str(tickerCIK[company]) +"&type=10-K%25&dateb=&owner=exclude&start=0&count=40&output=atom"
#print(url)
xml = requests.get(url)
soup = BeautifulSoup(xml.content, 'lxml')
tenKs = soup.find_all('filing-href')



kurl = tenKs[0].text
file = requests.get(kurl)
soup = BeautifulSoup(file.content, 'html')

kurls = [i['href'] for i in soup.find_all('a', href=True)]
docURL = "https://www.sec.gov/" + kurls[9]

print(docURL)

