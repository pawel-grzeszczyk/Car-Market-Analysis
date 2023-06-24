# **Car Market Analysis**

Please consider that this repository is still being developed.

## **Project overview**:

### **Main goals**:

1. Determining how and to what extent car parameters affect its value.
2. Identifying which parameters have a statistically significant impact on the price of a car.
3. Selecting the best machine learning model for car valuation.

### **Steps:**

1. **Data aquisition** ✅

   Building web scraping program and using it to gather real data.

2. **Data cleaning** ❌

   Due to the fact that the scraped data is sourced from the internet and was self-filled by website users, it will require thorough cleaning.

3. **Quantitative analysis** ❌

   Familiarizing oneself with the data and discovering its structure through data aggregation and visualization.

4. **Price analysis** ❌

   Checking the distribution of car prices and conducting a basic analysis to determine how car parameters influence its price.

5. **Statistical analysis** ❌

   Determining which parameters of the car have a statistically significant impact on its price.

6. **ML models development and evaluation** ❌

   Development, optimization, and evaluation of various machine learning algorithms for car valuation based on its parameters.

7. **Selection of the best model** ❌

   Comparison of model results and selection of the best performing model

### **Project files:**

**`car_market_analysis.ipynb`**

Old analysis file which will be replaced in the comming days.

**Data Scraping (step 1)**

- **`links_scraper.py`**

  Used to scrape and extract links from the car market website 'https://www.otomoto.pl'. Scraper iterates over pages for specified brands, gathers offer links and saves them in .csv file. The script utilizes the requests library to send HTTP requests, the BeautifulSoup library for HTML parsing, and the re library for regular expression matching. It also employs the tqdm library to provide a progress bar during the scraping process.

- **`data_scraper.py`**

  This Python script iterates over the specified brands and reads the previously scraped links (by `links_scraper.py`) from CSV files. It divides the links into iterations of 1000 links each and retrieves the car data from the corresponding web pages. The extracted data includes parameters such as vehicle brand, model, production year, mileage, engine capacity, fuel type, power, gearbox, price, etc.The retrieved data is then saved in separate CSV files for each brand and iteration. Each CSV file contains rows representing individual car offers, and the columns correspond to the parameters mentioned above.

**Data Cleaning (step 2)**

**Data Analysis (steps 3, 4, 5)**

**Machine Learning (steps 6, 7)**
