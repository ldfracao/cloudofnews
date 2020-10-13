import requests
from bs4 import BeautifulSoup

text = ""
html_folha_en = requests.get("https://www1.folha.uol.com.br/internacional/en/scienceandhealth/2020/10/national-force-helicopter-crashes-in-pantanal-and-leaves-three-injured.shtml")
folha_en_text = html_folha_en.text
soup = BeautifulSoup(folha_en_text, "lxml")

text = soup.find_all('time')
print(text)