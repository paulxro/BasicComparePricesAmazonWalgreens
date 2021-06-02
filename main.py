import requests
from bs4 import BeautifulSoup
import re

myDivs = None
keywords = input("Enter key words: ").split()
baseUrls =  ["https://www.walmart.com/search/?query=","https://www.amazon.com/s?k=", "https://www.walgreens.com/search/results.jsp?Ntt="]
newUrls = []
finalPrices = []
actualUrls = []
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

for url in baseUrls:
  url += keywords[0]
  for index, keyword in enumerate(keywords):
    if index != 0: url += "+" + keyword
  newUrls.append(url)
r = requests.get(newUrls[1], headers = headers)
page = BeautifulSoup(BeautifulSoup(r.content, 'html.parser').prettify(), 'html.parser')
myDivs = page.find("a", class_="a-link-normal a-text-normal")
try:
  if str(myDivs).split()[3][:9] != 'href="/gp':
    newLink = str(myDivs).split()[3][len("href=**"):str(myDivs).split()[3].find("/ref")]
    actualUrls.append("https://amazon.com/" + newLink)
    #print("https://amazon.com/" + newLink)
  else:
    newLink = str(myDivs).split("%2F")[1] + "/dp/" + str(myDivs).split("%2F")[3]
    actualUrls.append("https://amazon.com/" + newLink)
    #print("https://amazon.com/" + newLink)
  r2 = requests.get("https://amazon.com/" + newLink, headers = headers)
  page2 = BeautifulSoup(BeautifulSoup(r2.content, 'html.parser').prettify(), 'html.parser')
  finalPrices.append(float(page2.find(id="priceblock_ourprice").getText()[1:].replace(",",""))) if page2.find(id = "priceblock_ourprice") != None else finalPrices.append(float(page2.find(id="priceblock_saleprice").getText()[1:].replace(",","")))
except:
  print("Sorry, something went wrong with the Amazon link.")
r = requests.get(newUrls[2], headers = headers)
page = BeautifulSoup(BeautifulSoup(r.content, 'html.parser').prettify(), 'html.parser')
try: 
  preLink = str(page.find("a", id=lambda x: x and x.startswith('title-secondary-0compare_sku'))).split()[2][7:]
  linkFinal = "https://www.walgreens.com/" + preLink[:len(preLink)-1]
  actualUrls.append(linkFinal)
  r2 = requests.get(linkFinal, headers = headers)
 
  page2 = BeautifulSoup(BeautifulSoup(r2.content, 'html.parser').prettify(), 'html.parser')
  basePriceReference = str(page2.find("span", class_="product__price")).split("<span>")[1].split("\n")
  finalPrices.append(int(basePriceReference[1].split()[0]) + float(basePriceReference[4].split()[0])/100)
except:
  print("Sorry, something went wrong with the Walgreens link.")

for price, url  in zip(finalPrices,actualUrls):
  print("Item was found at " + url + " for $" + str(price))
