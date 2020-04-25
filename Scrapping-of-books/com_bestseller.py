import requests
import bs4
import csv
# Getting main page from amazon.com bestsellers website
get_url = 'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/'
main_page = requests.get(get_url)
main_page_soup = bs4.BeautifulSoup(main_page.text, 'lxml')
pages_list = main_page_soup.select('.zg_page')

pages_links_list = []

# Getting all pages
for i in pages_list:
    pages_links_list.append(i.find('a').get('href'))

authors = []
links = []
prices = []
names = []
ratings = []
num_ratings = []

# Getting Selectors for the required fields
for link in pages_links_list:
    res = requests.get(link)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    main = soup.select('.zg_itemWrapper')
    for i in main:
        try:
            authors.append(i.select('.a-link-child')[0].text)
        except:
            try:
                authors.append(i.select('.a-color-base')[0].text)
            except:
                authors.append('Not available')

        try:
            links.append(i.find('a').get('href'))
        except:
            links.append('Not available')

        try:
            names.append(i.select('.p13n-sc-truncate')[0].getText().strip())
        except:
            names.aapend('Not available')

        try:
            prices.append(i.select('.p13n-sc-price')[0].text.strip())
        except:
            prices.append('Not available')

        try:
            temp = i.select('.a-icon-row')[0]
            # ratings.append(i.select('.a-icon-row')[0].select('.a-link-normal')[0].get('title'))
            # num_ratings.append(i.select('.a-icon-row')[0].select('.a-size-small')[0].text)
            ratings.append(temp.select('.a-link-normal')[0].get('title'))
            num_ratings.append(temp.select('.a-size-small')[0].text)
        except:
            ratings.append('Not available')
            num_ratings.append('Not available')

# Finalising the Lists with small corrections
for i in range(len(num_ratings)):
    num_ratings[i] = num_ratings[i].replace(u',', u'')
    if num_ratings[i] != 'Not available':
        num_ratings[i] = int(num_ratings[i])

    links[i] = 'https://www.amazon.com' + links[i]


# Declaring header list
title_list = ['Name', 'URL', 'Author', 'Price',
              'Number of Ratings', 'Average Rating']

# Writting to csv file
with open('./output/com_book.csv', 'w', encoding='utf-8') as inpfil:
    csv_writer = csv.writer(inpfil)
    csv_writer.writerow(title_list)
    for i in range(len(names)):
        csv_writer.writerow([names[i]] + [links[i]] + [authors[i]] +
                            [prices[i]] + [num_ratings[i]] + [ratings[i]])
