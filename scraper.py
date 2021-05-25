from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import time
import sqlite3
import os.path

# creates database file if none exist and configures database connection
if os.path.exists('coinmarketcap_scraper_db.db'):
    try:
        dbConn = sqlite3.connect('coinmarketcap_scraper_db.db')
        print("Connected to database successfully")
    except Exception as e:
        print("Error during database connection: ", str(e))
else:
    print("Creating new database from schema backup...")
    open('coinmarketcap_scraper_db.db', 'x')
    try:
        dbConn = sqlite3.connect('coinmarketcap_scraper_db.db')
        print("Connected to database successfully")
    except Exception as e:
        print("Error during database connection: ", str(e))

# creates database cursor to execute SQL scripts
cursor = dbConn.cursor()

# ensures proper tables exist within the database
dbSchema = open('coinmarketcap_scraper_db_schema.sql')
dbSchemaString = dbSchema.read()
cursor.executescript(dbSchemaString)

# define target URL to scrape
url_to_scrape = "https://coinmarketcap.com/"

# uses Chrome driver to get entire page and scroll to load JS generated HTML <tr> elements
chrome_path = "./chromedriver.exe"
# runs Chrome without the UI to load the JS generate HTML
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_path, options=options)
driver.set_window_size(1920, 1080)
driver.get(url_to_scrape)
# scrolls the page, allowing time for each chunk's JS to generate the necessary <tr> data via time.sleep()
for i in range(0, 8):
    driver.execute_script("window.scrollBy({top:1500,left:0,behavior: 'smooth'})")
    time.sleep(1)
    print(f"Parsing chunk {i}/7...")
page_html = driver.page_source
driver.quit()

# parses page source for each table row
html_soup = BeautifulSoup(page_html, 'html.parser')
currency_items = html_soup.find('body').find('table').find_all('tr')

# creates and opens file to hold results
results = 'top100.csv'
f = open(results, 'w')

# write timestamp and header to results file
dtCurrent = 'TIMESTAMP: {:%Y-%b-%d %H:%M:%S}\n'.format(datetime.datetime.now())
header = 'Rank#, Name, Symbol, Price, 24h %, 7d %, Market Cap, Volume (24h), Circulating Supply \n'
f.write(dtCurrent)
f.write(header)

# scrape currency data for each and write to file
for i in range(1, len(currency_items)):
    # name scrape:
    name = currency_items[i].find_all('p')[1].text

    # prints a line to reveal current currency being scraped
    print("********")
    print(f"Scraping {name}")

    # symbol scrape
    symbol = currency_items[i].find_all('p')[2].text

    # price scrape:
    price = currency_items[i].find_all('a')[1].text

    # 24h % scrape:
    oneDayDeltaP = currency_items[i].find_all('span')[2].text

    # 7d % scrape:
    svnDayDeltaP = currency_items[i].find_all('span')[4].text

    # Market Cap scrape:
    mCap = currency_items[i].find_all('p')[3].find_all('span')[1].text

    # Day Volume scrape:
    dayVol = currency_items[i].find_all('p')[4].text

    # Circulating Supply scrape:
    cSupply = currency_items[i].find_all('p')[5].text

    # writes data for each currency to results file 
    f.write(f"#{i}:, {name}, {symbol}, {price}, {oneDayDeltaP}, {svnDayDeltaP}, {mCap}, {dayVol}, {cSupply}\n")

    # inserts data for each currency to database tables (expect errors from attempts to save duplicate entries to "currencies" data)
    try:
        cursor.execute(f'INSERT INTO "main"."currencies"("name","symbol") VALUES ("{name}","{symbol}")')
    except Exception as e:
        print(str(e))
        print(f'{name} already exists in "currencies" table...ignoring')

    cursor.execute(f'INSERT INTO "main"."market_data"("price","24h%","7d%","market_cap","volume_24h","supply","symbol") VALUES ("{price}","{oneDayDeltaP}","{svnDayDeltaP}","{mCap}","{dayVol}","{cSupply}","{symbol}");')

    # prints a line on completion of each currency scrape
    print(f"Finished scraping {name}!")
    print("********")

# closes the results file
f.close()

# closes database connection
if dbConn:
    dbConn.commit()
    dbConn.close()
    print("Connection to database has been closed")
