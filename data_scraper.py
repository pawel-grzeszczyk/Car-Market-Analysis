def data_scraper():
  import csv 
  from bs4 import BeautifulSoup
  from numpy import NaN 
  import requests
  import pandas as pd
  import const

  links = pd.read_csv('datasets/offer_links_tesla.csv', header=None)

  # paramteres that I'm looking for in the offers
  colnames = ['brand', 'model', 'production_year', 'mileage[KM]', 'fuel_type', 'power[HP]', 'gearbox', 'door_no', 'seat_no', 'color',
              'origin_country', 'status']

  # prices list
  prices = []

  # connecting to links and getting information from them
  for link in links[0]:
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'lxml')

    # prices values
    price = soup.find('span', class_='offer-price__number')
    try:
      prices.append(price.text)
    except:
      prices.append(NaN)

    # objects where data about parameters are stored
    params = soup.find_all('li', class_='offer-params__item')

    # finding labels and values of paramters and creating a dictionary from them
    categories = [i.find("span", class_="offer-params__label").text for i in params]

    values = [i.find("div", class_="offer-params__value").text.strip() for i in params]
        
    offer_data = {i:j for i, j in zip(categories, values)}

    keys = ['Marka pojazdu', 'Model pojazdu', 'Rok produkcji', 'Przebieg', 'Rodzaj paliwa', 'Moc', 'Skrzynia biegów', 
            'Liczba drzwi', 'Liczba miejsc', 'Kolor', 'Kraj pochodzenia', 'Stan']

    # selecting values that I'm looking for and creating a dictionary
    row = []

    for key in keys:
      try:
        row.append([offer_data.get(key)])
      except:
        row.append([NaN])

    offer_dictionary = {i:j for i,j in zip(colnames, row)}
    
    try:
      df = pd.concat([df, pd.DataFrame(offer_dictionary)], ignore_index=True)
    except:
      df = pd.DataFrame(offer_dictionary)

  # adding prices column to the df
  df['price[PLN]'] = prices

  # saving the data to csv file
  df.to_csv('datasets/data_{}.csv'.format(const.brand), index=False)