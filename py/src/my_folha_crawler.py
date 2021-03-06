from bs4 import BeautifulSoup 
from elasticsearch import Elasticsearch
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
import requests
import re
import validators

client = Elasticsearch("http://localhost:9200")
response = requests.get("https://www1.folha.uol.com.br/internacional/en/")
html = response.text
soup = BeautifulSoup(html, "lxml")

requestedUrls = ["https://www1.folha.uol.com.br/internacional/en/"]

def crawl(arg):
    # finds tag that identifies page as a news article
    findNews = arg.find(attrs={"property" : "article:published_time"})
    if findNews:
        findDate = findNews["content"]
        findDate = re.sub(r"\s.*", "", findDate)

        link = arg.find("link")["href"]

        # find relevant paragraphs
        allps = []
        notps = []
        textps = []

        # finds ps with attributes
        for i in arg.find_all("p" , attrs = {re.compile("."), re.compile(".")}):
                notps.append(i)
        # finds ps that don't have or have children as tags <br>, <strong> or <b>
        for i in arg.find_all("p"):
            if bool(i.find()) is False or i.find("br") or i.find("strong") or i.find("b"):
                allps.append(i)
        # if p has a child of sup or sub remove it, in case not pass
            try:
                if i.find("sup") or i.find("sub") or i.find("a"):
                    allps.remove(i)
            except:
                pass
        # removes empty paragraphs contained in some pages
            try:
                if re.match("^â", i.text):
                    allps.remove(i)
            except:
                pass

        allps = allps[:-2]  # removes the last 2 paragraphs
        allps = list(set(allps) - set(notps))   # excludes unwanted ps

        # grabs the text of ps in the right encoding
        for i in allps:
            i = i.text.encode("latin-1", "ignore").decode("utf-8", "ignore")
            textps.append(i)

        # find relevant headers
        headers = []
        for i in arg.find_all("h1"):
            headers.append(i.text.encode("latin-1").decode("utf-8").strip())
        for i in arg.h2:
            headers.append(i.encode("latin-1").decode("utf-8").strip())

        headers = headers[2:]
        textps = textps + headers

        # removes possible duplicates 
        text_clean = []
        for i in textps:
            if i not in text_clean:
                text_clean.append(i)
        text_clean = str(text_clean)
        text_clean = text_clean.replace("\\n", "").replace("\\r", " ").replace("\\u200b", "").replace("\\", "")

        # elasticsearch integration
        doc = { "date" : findDate, "string" : text_clean , "links" : link}
        client.index( "cloudofnews", doc )

        # wordcloud
        # wc = WordCloud()
        root_path = "/home/pimblus/Documents/cloud-of-news-v1.1/"
        custom_mask = np.array(Image.open(root_path + "imgs/mask3.jpg"))
        wc = WordCloud(background_color="black", mask=custom_mask)
        wc.generate(text_clean)
        wc.to_file(root_path + 'imgs/cloudstest/' + findDate + '.png')

    else:
        # finds all href attributes
        hrefs = []
        for i in arg.find_all("a", href = True):
            hrefs.append(i.attrs["href"])

        # validates hrefs as urls 
        validUrls = []
        for x in hrefs:
            hrefs = validators.url(x)
            if hrefs is True:
                validUrls.append(x)

        # removes duplicates
        urls_clean = []
        for i in validUrls:
            if i not in urls_clean:
                urls_clean.append(i)

        # filters links 
        filterArr = []
        for i in urls_clean:
            if re.match("^htt(p|ps)://www1.folha.uol.com.br/internacional/en/.*/", i):
                filterArr.append(i)
                if re.match("^htt(p|ps)://www1.folha.uol.com.br/internacional/en/ombudsman.*", i):
                    filterArr.remove(i)
                if re.match("^htt(p|ps)://www1.folha.uol.com.br/internacional/en/opinion.*", i):
                    filterArr.remove(i)
                if re.match("^htt(p|ps)://www1.folha.uol.com.br/internacional/en/.*newsen$", i):
                    filterArr.remove(i)
                try:
                    if re.match("^htt(p|ps)://www1.folha.uol.com.br/internacional/en/.*opinion.*", i):
                        filterArr.remove(i)
                except:
                    pass

        # soupifies all valid and filtered links 
        newSoup = []
        for i in filterArr:
            if i not in requestedUrls:
                requestedUrls.append(i)
                innerResponse = requests.get(i)
                i = innerResponse.text
                newSoup = BeautifulSoup(i, "lxml")
                newSoup.append(i)
                crawl(newSoup)

crawl(soup)
