import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import validators

response = requests.get("https://www1.folha.uol.com.br/internacional/en/")
html = response.text
soup = BeautifulSoup(html, "lxml")

# finds tag that identifys page as a news article
findNews = soup.find(attrs={"property" : "article:published_time"})
if bool(findNews) is True:
    findDate = findNews["content"]
    findDate = re.sub(r"\s.*", "", findDate)

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
validUrls = np.array(validUrls)
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
    innerResponse = requests.get(i)
    i = innerResponse.text
    soup = BeautifulSoup(i, "lxml")
    newSoup.append(i)
newSoup = np.array(newSoup)
print(newSoup)
print(len(newSoup))
# print(type(newSoup))















# for i in urls_clean:
#     urls_clean.remove("https://www1.folha.uol.com.br/internacional/en/opinion/")
# print(urls_clean)


# print(validUrls)

# for i in urls_clean:

# hrefs = []
# validHrefs = []
# for x in soup.find_all('a', href=True):
#     hrefs.append(x)

# print(hrefs)


# validUrls = []
# for x in validHrefs:
#     valid = validators.url(x)
#     if valid is True:
#         validUrls.append(x)
#     else:
#         continue

    # print ("Found the URL:", validUrls)


# for x in links:
#     req = requests.get(links)
#     serverResponse.append(req)
    
# serverResponse.append(requests.get(links))
# if serverResponse == 200:
#     serverResponse.append(serverResponse)

# if serverResponse == 200:
#     serverResponse.append(links)
# for x in links
#     print(x)
    # serverResponse.append(requests.get(links))
    # if serverResponse == 200:
    #     newHtml = []
    #     newHtml.append().content
# getHtml = serverResponse.content
   


    
# timeTag = soup.find_all("time")
# print(timeTag)

# links = []
# for a in soup.find_all('a', href=True):
#     links.append(a['href'])

# print(links)
    # print ("Found the URL:", a['href'])











# text = ""
# text1 = ""
# html_folha_en = requests.get("https://www1.folha.uol.com.br/internacional/en/")
# folha_en_text = html_folha_en.text
# soup = BeautifulSoup(folha_en_text, "lxml")

# bytag = soup.find_all('time')


# print(bytag)