from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import nltk

nltk_stopwords = nltk.corpus.stopwords.words('portuguese')
custom_stopwords = ["diz","atuam","claro","pode","sobre","primeira","quer","haver","têm"]

stopwords = nltk_stopwords + custom_stopwords

root_path = "/home/infinity/cloud-of-news/"

text = ""
with open(root_path + 'data/web-crawler-manual.txt', encoding='utf-8') as f:
    text = ''.join(f.readlines())

text = text.replace('\n','')

text_list = text.lower().split(' ')
text_clean = ""
for w in text_list:
    if not w in stopwords:
        text_clean = text_clean + ' ' + w

wc = WordCloud()

custom_mask = np.array(Image.open(root_path + "imgs/latin-america-black-white-vector-croped.jpg"))
wc = WordCloud(background_color="black", mask=custom_mask)
wc.generate(text_clean)
wc.to_file(root_path + 'imgs/test1.png')
