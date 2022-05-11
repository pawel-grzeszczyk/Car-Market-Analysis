def links_scraper():
    from bs4 import BeautifulSoup # makes the HTML data more readable and easy to deal with
    import requests # connecting to website
    import regex as re # regular expressions
    import csv # used to sace file in the csv
    import os # used to detect file directory to delete file if exists
    import const

    brand = const.brand

    page_no = 1
    link_list = []

    # Finding the last page on the website
    try:
        print('Searching offers for brand {}.'.format(brand))
        print('...')

        URL = 'https://www.otomoto.pl/osobowe/{}'.format(brand)

        page = requests.get(URL).text

        soup = BeautifulSoup(page, 'lxml')
    except:
        print('No internet connection. Ending program\n')
        quit()

    try:
        pages = str(soup.find('ul', class_='pagination-list').find_all('li'))

        last_page = re.findall('Page [0-9]*', pages)[-1].split()[-1]

        last_page = int(last_page)
    except:
        last_page = 1

    # iterating over pages and reading data from them until the last read page = last page
    while (page_no <= last_page):
        URL = 'https://www.otomoto.pl/osobowe/{}?page={}'.format(brand, str(page_no))

        page = requests.get(URL).text

        soup = BeautifulSoup(page, 'lxml')

        for article in soup.find_all('article'):
            link = article.a.get('href')
            
            if re.search('https://www.otomoto.pl/oferta/', link):                                 
                link_list.append(link)   
        page_no += 1  

    print('Found {} links on {} pages for {}.'.format(len(link_list), (page_no-1), brand))
    # print(link_list)

    # Checking if there are any duplicates in a list and getting rid of them
    def checkIfDuplicates(test_list):
        if len(test_list) == len(set(test_list)):
            print('No duplicates found.')
            print('Found {} unique values.'.format(len(test_list)))
            return
        else:
            deleted = len(test_list) - len(set(test_list))
            test_list = list(set(test_list))
            print('Found {} duplicates and got rid of them.'.format(deleted))
            print('Found {} unique values.'.format(len(test_list)))
            return

    checkIfDuplicates(link_list)

    # removing file where the data is to be saved (if already exists)
    file_name = 'datasets/offer_links_{}.csv'.format(const.brand)

    if(os.path.exists(file_name) and os.path.isfile(file_name)):
        os.remove(file_name)

    # creating a csv writer to save downloaded data into the csv file
    csv_file = open(file_name, "w", newline='')
    writer = csv.writer(csv_file)

    # saving the data
    for value in link_list:
        writer.writerow([value])

    csv_file.close()