import requests
import bs4

url = 'http://www.andhrabhoomi.net/content/ap-14466'

pg = requests.get(url)
sp = bs4.BeautifulSoup(pg.text, 'lxml')

element = sp.find('div', {"class": "field field-name-body field-type-text-with-summary field-label-hidden"})
# element = sp.find('div', {'class': 'field-item even'})
paras = element.find_all('p')

text = ''

for para in paras:
    text += para.text + '\n'

print(text)