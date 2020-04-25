import requests
from bs4 import BeautifulSoup

url = 'https://cinema.suryaa.com/latest-cinema-telugu-news.html?pagination='

for i in range(1, 2):
    # if i%10==0:
    # 	time.sleep(20)
    all_links = []
    url_page = url + str(i)
    # print(url_page)
    r = requests.get(url_page)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    main_body = soup.find('div', {"class": "single_category"})
    elements = soup.find_all('div', {"class": "media-body"})
    for link in elements:
        all_links.append(link.find('a').get('href'))
    print(all_links)
    for l in all_links:
        print(l)
