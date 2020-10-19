import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import validators

response = requests.get("https://www1.folha.uol.com.br/internacional/en/business/2020/10/brazil-lags-behind-chile-uruguay-and-argentina-in-development-ranking.shtml?utm_source=newsletter&utm_medium=email&utm_campaign=newsen")
html = response.text
html = html.replace(",", "").replace("\"", "").replace("\n", "").replace("\r", "")
soup = BeautifulSoup(html, "lxml")

requestedUrls = ["https://www1.folha.uol.com.br/internacional/en/"]

# finds tag that identifies page as a news article
findNews = soup.find(attrs={"property" : "article:published_time"})
if bool(findNews) is True:
    findDate = findNews["content"]
    findDate = re.sub(r"\s.*", "", findDate)

    # find relevant paragraphs
    allps = []
    for i in soup.find_all("p"):
        allps.append(i.text)
    allps = allps[:-6]
    # print(allps)
    # print(len(allps))
    
    # find relevant headers
    headers = []
    for i in soup.find_all(["h1", "h2"]):
        headers.append(i.text.strip())
    headers = headers[2:]
    # print(headers)
    # print(len(headers))

    text = allps + headers
   
    # print(text)
    # print(len(text))
    # removes possible duplicates 
    text_clean = []
    for i in text:
        if i not in text_clean:
            text_clean.append(i)

    # print(text_clean)
    # print(len(text_clean))

# finds all href attributes
hrefs = []
for i in soup.find_all(href = True):
    hrefs.append(i.attrs["href"])
# hrefs = np.array(hrefs)
# print(hrefs)
# print(len(hrefs))

# validates hrefs as urls 
validUrls = []
for x in hrefs:
    hrefs = validators.url(x)
    if hrefs is True:
        validUrls.append(x)
# validUrls = np.array(validUrls)
# print(validUrls)
# print(len(validUrls))

# removes duplicates
urls_clean = []
for i in validUrls:
    if i not in urls_clean:
        urls_clean.append(i)
# urls_clean = np.array(urls_clean)
# print(urls_clean)
# print(len(urls_clean))

# filters links 
filterArr = []
for i in urls_clean:
    if re.match("^https://www1.folha.uol.com.br/internacional/en/", i):
        filterArr.append(i)    
# filterArr = np.array(filterArr)
# print(filterArr)
# print(len(filterArr))

# soupifies all valid and filtered links 
newSoup = []
for i in filterArr:
    if i not in requestedUrls:
        innerResponse = requests.get(i)
        requestedUrls.append(i)
        i = innerResponse.text
        i = i.replace(",", "").replace("\"", "").replace("\n", "").replace("\r", "")
        newSoup = BeautifulSoup(i, "lxml")
        newSoup.append(i)
# newSoup = np.array(newSoup)
# print(requestedUrls)
# print(len(requestedUrls))

# print(newSoup)
# print(len(newSoup))
# print(type(newSoup))
