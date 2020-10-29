import requests
from bs4 import BeautifulSoup
import re
from elasticsearch import Elasticsearch
import json
import pymysql.cursors

response = requests.get("https://www1.folha.uol.com.br/internacional/en/saopaulo/2018/08/needlework-brings-hope-back-in-tremembe-womens-prison.shtml")
html = response.text
soup = BeautifulSoup(html, "lxml")
# print(soup.original_encoding)
requestedUrls = ["https://www1.folha.uol.com.br/internacional/en/"]

findNews = soup.find(attrs={"property" : "article:published_time"})
if findNews:
    findDate = findNews["content"]
    findDate = re.sub(r"\s.*", "", findDate)

    # find relevant paragraphs
    allps = []
    notps = []
    textps = []

    # finds ps with attributes
    for i in soup.find_all("p" , attrs = {re.compile("."), re.compile(".")}):
            notps.append(i)
    # finds ps that don't have children and with <br> as a child
    for i in soup.find_all("p"):
        if bool(i.find()) is False or i.find("br") or i.find("strong"):
            allps.append(i)
    # if p has a child of sup or sub remove it, in case not pass
        try:
            if i.find("sup") or i.find("sub"):
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

    # grabs the text of ps
    for i in allps:
        textps.append(i.text)

    # find relevant headers
    headers = []
    for i in soup.find_all("h1"):
        headers.append(i.text.strip())
    for i in soup.h2:
        i = i.strip()
        headers.append(i)
    headers = headers[2:]

    textps = textps + headers

    # removes possible duplicates 
    text_clean = []
    for i in textps:
        if i not in text_clean:
            text_clean.append(i)
    text_clean = str(text_clean)
    text_clean = text_clean.replace(".", "").replace(",", "").replace("(", "").replace(")", "").replace("'", "").replace("\"", "").replace("[", "").replace("]", "")
    print(text_clean)
    print(type(text_clean))
    # text_clean = json.dumps(text_clean)
    # print(text_clean)
    # print(type(text_clean))

    client = Elasticsearch("http://localhost:9200")

    doc = { "date" : findDate, "string" : text_clean }

    # datedoc = { "date" : findDate }

    client.index( "testindex", doc )
    # client.indices.delete("testindex")
    # client.indices.delete("date")
    # client.index( "date", datedoc )
    # print(dir(client))
    # print(text_clean)
    # print(type(text_clean))
    # res = requests.post("http://localhost:9200/testindex/", data="text" , json=text_clean)
    # print(res)

    # (/{index}/_doc/{id}, /{index}/_doc, or /{index}/_create/{id}) 
    # server connection
    # conn = pymysql.connect(
    #     host='localhost',
    #     user='pimblus',
    #     database='testdb',
    #     passwd='Gv34@-aT'
    # )
    # try:
    #     with conn.cursor() as cursor:
    #         sql = "SELECT Date FROM crawl WHERE Date = %s;"
    #         val = (findDate)
            # sentence = cursor.execute(sql, val)
            # print(sentence)
            # print(type(sentence))
            # print(sql)
            # if sentence is True:
                
                # query = "INSERT INTO crawl (Date, String) VALUES (%s, %s);"
                # query = "UPDATE crawl SET Date = %s, String = %s;"
                # val = (findDate, text_clean)
                # cursor.execute(query, val)
            # else:
                # INSERT NEW FIELD
    #     conn.commit()
    # finally:
    #     conn.close()
  