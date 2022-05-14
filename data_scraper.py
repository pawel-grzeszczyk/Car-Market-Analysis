def data_scraper():
  import csv 
  from bs4 import BeautifulSoup
  from numpy import NaN 
  import requests
  import pandas as pd
  import const

    
  links = pd.read_csv('datasets/offer_links_{}.csv'.format(const.brand), header=None)

  with open('datasets/data_{}.csv'.format(const.brand), 'w', encoding='utf8', newline='') as f:
    thewriter = csv.writer(f)

    # colnames
    colnames = ['brand', 'model', 'production_year', 'mileage[KM]', 'fuel_type', 'power[HP]', 'gearbox', 'door_no', 'seat_no', 'color',
                'origin_country', 'status']
    thewriter.writerow(colnames)

    # prices list
    prices = []
    price_ix = 0

    # connecting to links and getting information from them
    for link in links[0]:
      page = requests.get(link).text
      soup = BeautifulSoup(page, 'lxml')

      # prices values
      price = soup.find('span', class_='offer-price__number')
      try:
        prices.append(price.text.strip())
      except:
        prices.append(NaN)

      # objects where data about parameters are stored
      params = soup.find_all('li', class_='offer-params__item')

      # finding labels and values of paramters and creating a dictionary from them
      categories = [i.find("span", class_="offer-params__label").text for i in params]

      values = [i.find("div", class_="offer-params__value").text.strip() for i in params]
                
      offer_data = {i:j for i, j in zip(categories, values)}

      # defining values that I'll be looking for in a dictionary
      keys = ['Marka pojazdu', 'Model pojazdu', 'Rok produkcji', 'Przebieg', 'Rodzaj paliwa', 'Moc', 'Skrzynia biegów', 
              'Liczba drzwi', 'Liczba miejsc', 'Kolor', 'Kraj pochodzenia', 'Stan']

      # creating a list for each offer
      row = []

      for key in keys:
        try:
          row.append([offer_data.get(key)][0])
        except:
          row.append([NaN])

      # adding prices to the corresponding offers     
      row.append(prices[price_ix])
      price_ix += 1

      #saving each row in a csv file
      thewriter.writerow(row)