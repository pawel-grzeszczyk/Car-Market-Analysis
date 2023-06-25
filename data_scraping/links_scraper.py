import requests
from bs4 import BeautifulSoup
import re
import csv
from tqdm import tqdm

# audi, bmw, ford, mercedes-benz, opel, peugeot, renault, skoda, toyota, volkswagen
brands = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'peugeot', 'renault', 'skoda', 'toyota', 'volkswagen']

for i in brands:

    BRAND = i
    last_page = 1 # 1 for all pages

    # starting page number
    page_no = 0

    # list to store links
    link_list = []

    # iterate over pages
    while page_no < last_page:
        for page_no in tqdm(range(last_page)):
            page_no += 1
            URL = f'https://www.otomoto.pl/osobowe/{BRAND}?page={page_no}'
            page = requests.get(URL).text
            soup = BeautifulSoup(page)

            if last_page == 1:
                try:
                    pagination = str(
                        soup.find('ul', class_='pagination-list').find_all('li'))
                    last_page = int(re.findall(
                        'Page [0-9]*', pagination)[-1].split()[-1])
                except:
                    last_page = 1
                print(
                    f'\nScrapping {last_page} pages of brand {BRAND.capitalize()}.')

            # iterate over ads to find their links
            for article in soup.find_all('h2'):
                try:
                    link = article.a.get('href')
                    if re.search('https://www.otomoto.pl/osobowe/oferta/', link):
                        link_list.append(link)
                except:
                    continue

                # open file to store links
                file_name = f'data_scraping/data/links/offer_links_{BRAND}.csv'
                csv_file = open(file_name, "w", newline='')
                writer = csv.writer(csv_file)

    # save the data
    print(
        f'Found {len(link_list)} links. There are {len(set(link_list))} unique links.')
    print('Saving the data...\n')
    for value in link_list:
        writer.writerow([value])

    csv_file.close()
