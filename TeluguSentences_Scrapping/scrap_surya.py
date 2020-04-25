import os
import threading

import requests
from bs4 import BeautifulSoup

url = 'https://www.telugu.suryaa.com/andhrapradesh-latest.php?pagination='
dir = 'politics_surya/'
if not os.path.isdir(dir):
    os.mkdir(dir)



# M=1

def get_data(all_links, i):
    # global M
    j = 1
    for link in all_links:
        # print(link)
        # print("\n")
        tel = requests.get(link)
        tel.encoding = 'utf-8'
        html_link = tel.text
        soup1 = BeautifulSoup(html_link, "lxml")
        link_context = soup1.find('div', {'single_page_content'})
        with open("./" + dir + str(i) + '_' + str(j) + ".txt", "w") as file:
            length = len(link_context.find_all('p'))
            for text in link_context.find_all('p'):
                to_write = text.text
                # print(to_write)
                sentence_speration = to_write.split('.')
                # file.write(str(to_write))
                for line in sentence_speration:
                    # print(line)
                    line = line.strip()
                    if line and line != '\n' and line != ' ':
                        file.write((str(line) + ".\n"))
            # [file.write(str(line)+"\n") if line for line in sentence_speration]
        file.close()
        j = j + 1
    print(i, 'page ended')


threads = []
for i in range(1, 2):
    # if i%50==0:
    # 	time.sleep(10)
    all_links = []
    url_page = url + str(i)
    r = requests.get(url_page)
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    main_body = soup.find_all('div', {"class": "media-body"})
    # r=requests.get(url_page)
    # html=r.text
    # soup=BeautifulSoup(html,"")
    # main_body=soup.find('div',{"id":"block-system-main"})
    # elements=main_body.find_all('div',{"class":"views-field-title"})
    for link in main_body:
        all_links.append(link.find('a').get('href'))
    # get_data(all_links)
    threads.append(threading.Thread(target=get_data, args=(all_links, i)))
    # link_thread.daemon=True
    try:
        threads[-1].start()
        # link_thread.join()
        print(i, ' page started')
    except Exception as e:
        print(e)
        exit(1)

for thr in threads:
    thr.join()
