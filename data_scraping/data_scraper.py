import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv
import http.client
from tqdm import tqdm

# audi, bmw, ford, mercedes-benz, opel, peugeot, renault, skoda, toyota, volkswagen
brands = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'peugeot', 'renault', 'skoda', 'toyota', 'volkswagen']

for i in brands:

    BRAND = i
    print(f'Scraping brand: {BRAND}')

    all_links = pd.read_csv(f'offer_links/offer_links_{BRAND}.csv',
                        header=None)[0]

    iterations_no = (len(all_links) // 1000) + 1
    print(f'There will be {iterations_no} iterations')

    for i in np.arange(iterations_no):
        if i == 0:
            start = 0
            end = 1000
        else:
            start = i * 1000 + 1
            end = (i+1) * 1000

        links = all_links[start:end]

        with open(f'data/data_{BRAND}_{i}.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = csv.writer(f)

            # colnames
            colnames = ['Marka pojazdu',
                        'Model pojazdu',
                        'Rok produkcji',
                        'Przebieg',
                        'Pojemność skokowa',
                        'Rodzaj paliwa',
                        'Moc',
                        'Skrzynia biegów',
                        'Napęd',
                        'Spalanie W Mieście',
                        'Typ nadwozia',
                        'Liczba drzwi',
                        'Liczba miejsc',
                        'Kolor',
                        'Kraj pochodzenia',
                        'Bezwypadkowy',
                        'Serwisowany w ASO',
                        'Stan',
                        'Cena']
            thewriter.writerow(colnames)

            # connecting to links and getting information from them
            for link, i in zip(links, tqdm(range(len(links)))):
                http.client._MAXHEADERS = 1000
                try:
                    page = requests.get(link).text
                except:
                    print('Could not reach the page: \n', link)
                    continue
                soup = BeautifulSoup(page, 'lxml')

                # prices values
                try:
                    price = soup.find(
                        'span', class_='offer-price__number').text.strip()
                except:
                    price = np.NaN

                try:
                    # objects where data about parameters are stored
                    params = soup.find('div', class_='parametersArea')

                    # finding labels and values of paramters and creating a dictionary from them
                    labels = [i.text for i in params.find_all(
                        "span", class_="offer-params__label")]
                    values = [i.text.strip() for i in params.find_all(
                        "div", class_="offer-params__value")]
                except:
                    continue

                offer_data = {i: j for i, j in zip(labels, values)}
                offer_data['Cena'] = price

                # defining values that I'll be looking for in a dictionary
                keys = colnames

                # creating a list for each offer
                row = []

                for key in keys:
                    try:
                        row.append([offer_data.get(key)][0])
                    except:
                        row.append([np.NaN])

                # saving each row in a csv file
                thewriter.writerow(row)
