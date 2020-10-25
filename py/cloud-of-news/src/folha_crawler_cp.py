import requests

from bs4 import BeautifulSoup
import re

import pymysql.cursors

response = requests.get("https://www1.folha.uol.com.br/internacional/en/saopaulo/2018/08/needlework-brings-hope-back-in-tremembe-womens-prison.shtml")
html = response.text
html = html.replace(",", "").replace("\"", "").replace("\n", "").replace("\r", "")
soup = BeautifulSoup(html, "lxml")
# print(soup.original_encoding)
requestedUrls = ["https://www1.folha.uol.com.br/internacional/en/"]

# def findsoup(soup):
    # finds tag that identifies page as a news article
findNews = soup.find(attrs={"property" : "article:published_time"})
if findNews:
    findDate = findNews["content"]
    findDate = re.sub(r"\s.*", "", findDate)
    # findDate = b"findDate"
    findDate = str(findDate)
    # print(findDate)
    # print(type(findDate))
    # print(datetuple)
    # print(type(datetuple))

    # find relevant paragraphs
    allps = []
    notps = []

    for i in soup.find_all("p" , attrs = {re.compile("."), re.compile(".")}):
            notps.append(i)
    for i in soup.find_all("p"):
        if (bool(i.find()) is False or i.find("br")):
            allps.append(i)    #.text.strip()
    for i in allps:
        if i.find("sup") or i.find("sub"):
            allps.remove(i)
    for i in allps:
        if re.match("^â", str(i.string)):
            allps.remove(i)
    allps = allps[:-2]
    # allps = list(set(allps) - set(notps))
    # allps = str(allps)
    # allps = allps.replace("<p>", "").replace("</p>", "").replace("<br/>", "")
        # if i.find(attrs={re.compile("."): re.compile(".")}):
        #     allps.remove(i)

    # allps = allps[:-6]
    # print(notps)
    # print(len(notps))
    print(allps)
    print(len(allps))
    # print(notps)
    # print(len(allps))
    # find relevant headers
    headers = []
    h2s = []
    for i in soup.find_all("h1"):
        headers.append(i.text.strip())
    for i in soup.h2:
        i = i.strip()
        h2s.append(i)
    headers = headers[2:]
    
    # print(headers)
    # print(h2s)
    # print(len(headers))

    text = allps + headers

    # print(text)
    # print(len(text))

    # removes possible duplicates 
    text_clean = []
    for i in text:
        if i not in text_clean:
            text_clean.append(i)
    # text_clean = b"text_clean"
    text_clean = str(text_clean)
    # texttuple = tuple(text_clean)
    # text_clean = text_clean.encode("utf-8")
    # print(text_clean)
    # print(type(texttuple))

    # server connection
    conn = pymysql.connect(
        host='localhost',
        user='pimblus',
        database='testdb',
        passwd='Gv34@-aT'
    )
    try:
        with conn.cursor() as cursor:
            sql = "SELECT Date FROM crawl WHERE Date = %s;"
            val = (findDate)
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
        conn.commit()
    finally:
        conn.close()
  