import os
import re

import bs4
import requests
from humanize import naturalsize

archives_url = 'http://nirdprojms.in/index.php/jrd/issue/archive'
login_url = 'http://nirdprojms.in/index.php/jrd/login/signIn'
num_pages = 2

# if you want to download the resetricted files, set log_user to true and set your username and password 
log_user = False
username = ''
password = ''

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition.

    :param cd: content-disposition of the file header
    :return: file name
    """
    if not cd:
        return None
    name = re.findall('filename=(.+)', cd)
    if len(name) == 0:
        return None
    return re.sub(r'[^\x00-\x7f]', r'', name[0].replace('"', ''))


def is_downloadable(content_type):
    """
    Returns whether the file is downloadable or not from the file's content-type

    :param content_type: content-type of the file header
    :return: True if the file is downloadable else False
    """
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def get_links(sup):
    art_links = []
    book_review_links = []
    arr = art_links
    for i in sup.find('div', {'id': 'content'}).children:
        if repr(i):
            # print(i)
            if isinstance(i, bs4.NavigableString):
                continue

            k = i.find('a', {'class': "file"})
            if k:
                # print(k.get('href'))
                arr.append(k.get('href'))

            if i.name == 'h4' and i.has_attr('class') and i['class'][
                0] == 'tocSectionTitle' and i.text == "Book Reviews":
                arr = book_review_links

    return art_links, book_review_links


def download(link):
    global session
    l = link.replace('view', 'download')
    file_headers = session.head(l, allow_redirects=True).headers

    filename = get_filename_from_cd(file_headers.get('content-disposition'))

    if is_downloadable(file_headers.get('content-type')):
        try:
            file_size = int(file_headers['content-length'])
        except:
            # print(filename, l, file_headers, )
            # broken_links.append(link)
            return -1
        print('\t\t\t' + filename, '(', naturalsize(file_size), ')',
              ' downloading... ', flush=True, sep='', end='')
        file = session.get(l, stream=True)
        chunk_size = 1024
        downloaded = 0
        with open(filename, 'wb') as f:
            for chunk in file.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # print('.', end='')
                downloaded_percentage = int((downloaded / file_size) * 100)
                # print('{0}% Completed'.format(downloaded_percentage),
                #       '\b'.rjust(12 + len(str(downloaded_percentage)), '\b'), end='',
                #       flush=True)
            print('completed')

        file.close()
        return 1
    else:
        return -2


def download_files(links, directory):
    global broken_links, not_downloadable

    mkcd(directory)

    for link in links:
        status = download(link)
        if status == -1:
            broken_links.append(link)
        elif status == -2:
            not_downloadable.append(link)

    os.chdir('..')


def mkcd(name):
    if not os.path.isdir(name):
        os.mkdir(name)
    os.chdir(name)


def get_soup(url):
    pg = session.get(url)
    return bs4.BeautifulSoup(pg.text, 'lxml')


home_dir = os.getcwd()

mkcd("files")
path_to_download = home_dir + '/files'

session = requests.Session()

if log_user:
    session.post(login_url, data={'username': username, 'password': password})

for pg_num in range(1, num_pages + 1):
    print(pg_num)

    soup = get_soup(archives_url + '?issuesPage=' + str(pg_num))
    blocks = soup.find_all('div', {'style': 'float: left; width: 100%;'})

    for block in blocks:

        year = block.find('h4', {'class': 'expandissueyear'}).text.replace('&nbsp', '')

        print(year, ':')
        os.chdir(path_to_download)
        mkcd(year)
        path_to_year = path_to_download + '/' + year

        issues = block.find_all("div", {"id": "issue"})
        issues_links = []
        issues_titles = []

        for issue in issues:
            issues_links.append(issue.find('a').get('href'))
            issues_titles.append(issue.find('a').text)

        for idx, (title, issue) in enumerate(zip(issues_titles, issues_links)):

            os.chdir(path_to_year)
            print('\t' + title, ':')
            mkcd(title)

            sp = get_soup(issue)
            article_links, book_links = get_links(sp)

            broken_links = []
            not_downloadable = []

            print("\t\tArticles :")
            download_files(article_links, "Articles")

            print("\t\tBook Reviews :")
            download_files(book_links, "Book Reviews")
