import json 

company = input("Enter a company: ")
f = open("company_tickers.json")
data = json.load(f)
tickerCIK = {}
for i, l in data.items():
    currTicker = l['ticker']
    currCIK = l['cik_str']
    tickerCIK[currTicker] = currCIK
tickerCIK[company] 
