from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import nltk
nltk_stopwords = nltk.corpus.stopwords.words('english')
import requests
from bs4 import BeautifulSoup
import re
#########
# FOLHA #
#########
root_path = "/home/infinity/cloud-of-news/"

text = ""
html_folha_en = requests.get("https://www1.folha.uol.com.br/internacional/en/")
folha_en_text = html_folha_en.text

#soup = BeautifulSoup(html_str)
soup = BeautifulSoup(folha_en_text)
for node in soup.findAll('h2'):
    text = text + " " + str(node.findAll(text=True))

for node in soup.findAll('p'):
    text = text + " " + str(node.findAll(text=True))

###################
# BRAZILIAN POST #
###################
html_brazilian_en = requests.get("http://www.thebrazilianpost.com.br/")
brazilian_en_text = html_brazilian_en.text

#soup = BeautifulSoup(html_str)
soup = BeautifulSoup(brazilian_en_text)
for node in soup.findAll('h2'):
    text = text + " " + str(node.findAll(text=True))

text = text.replace("\\n","").replace("[","").replace("]","").replace("'","")
text = text.replace('\n','')
text = re.sub(r"\s{2,}", " ", text)

custom_stopwords = ["de"]
stopwords = nltk_stopwords + custom_stopwords

text_list = text.lower().split(' ')
text_clean = ""
for w in text_list:
    if not w in stopwords:
        text_clean = text_clean + ' ' + w

wc = WordCloud()

custom_mask = np.array(Image.open(root_path + "imgs/latin-america-black-white-vector-croped.jpg"))
wc = WordCloud(background_color="black", mask=custom_mask)
wc.generate(text_clean)
wc.to_file(root_path + 'imgs/test1-en.png')
