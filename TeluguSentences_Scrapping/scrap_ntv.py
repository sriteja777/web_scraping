from bs4 import BeautifulSoup
import requests
import threading
import time
import os

url = 'https://www.ntvtelugu.com/category/andhra-pradesh-news?page='

dir = 'Andhrapradesh/'
if not os.path.isdir('Andhrapradesh'):
    os.mkdir('Andhrapradesh')

session = requests.session()
# M=1

def get_data(all_links, i):
    # global M
    j = 1
    # k=1
    for link in all_links:
        # print(link)
        # print("\n")
        # if k%29==0:
        # 	time.sleep(5)
        time.sleep(0.01)
        tel = session.get(link, headers=headers)
        html_link = tel.text
        soup1 = BeautifulSoup(html_link, "html.parser")
        link_context = soup1.find('div', {'class': 'post-text'})
        with open("./" + dir + str(i) + '_' + str(j) + ".txt", "w") as file:
            # length=len(link_context.find_all('p'))
            for text in link_context.find_all('p'):
                to_write = text.get_text()
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
    # k=k+1
    print(i, 'page ended')

headers = {'Host': 'www.ntvtelugu.com',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate, br',
           'DNT': '1',
           'Connection': 'keep-alive',
           'Cookie': 'varient_csrf_cookie=71edc5904de632cf509bd2baf27009de; ci_session=uoi2djs0drhr5p5ndknjroqv4nsggl8g',
# 'Cookie: varient_csrf_cookie=71edc5904de632cf509bd2baf27009de; ci_session=n4s9vcdo0fh46c5pkfr5evbej0edi0e0
           'Upgrade-Insecure-session': '1',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache'
           }
# page_header = headers.update({'Referer': 'https://www.ntvtelugu.com/category/andhra-pradesh-news?page=37'})
threads = []
print(session.headers)
# exit(1)
session.headers = headers
print(headers)
for i in range(37, 38):
    # if i%50==0:
    # time.sleep(10)
    all_links = []
    url_page = url + str(i)
    r = session.get(url_page, headers=headers)
    print('got page', flush=True)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    main_body = soup.find('div', {"class": "category-posts"})
    elements = main_body.find_all('div', {"class": "post-item-horizontal post-title"})
    for link in elements:
        all_links.append(link.find('a').get('href'))

    # for l in all_links:
    # 	print(l)

    # print(len(all_links))
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

