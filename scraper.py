from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# define target URL to scrape
url_to_scrape = "https://coinmarketcap.com/"

# uses chrome driver to load entire page + JS
chrome_path = "./chromedriver.exe"
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_path, options=options)
driver.set_window_size(1920, 1080)
driver.get(url_to_scrape)
for i in range(0, 8):
    driver.execute_script("window.scrollBy({top:1500,left:0,behavior: 'smooth'})")
    time.sleep(1)
page_html = driver.page_source
driver.quit()

# parses page source for each table row
html_soup = BeautifulSoup(page_html, 'html.parser')
currency_items = html_soup.find('body').find('table').find_all('tr')

# creates and opens file to hold results
results = 'top100.csv'
f = open(results, 'w')

# write header to results file
header = 'Rank#, Name, Price, 24h %, 7d %, Market Cap, Volume (24h), Circulating Supply \n'
f.write(header)

# scrape currency data for each and write to file
for i in range(1, len(currency_items)):
    # name scrape:
    name = currency_items[i].find_all('p')[1].text

    # price scrape:
    price = currency_items[i].find_all('a')[1].text

    # 24h % scrape:
    oneDayDeltaP = currency_items[i].find_all('span')[2].text

    # 7d % scrape:
    svnDayDeltaP = currency_items[i].find_all('span')[4].text

    # Market Cap scrape:
    mCap = currency_items[i].find_all('p')[3].text

    # Day Volume scrape:
    dayVol = currency_items[i].find_all('p')[4].text

    # Circulating Supply scrape:
    cSupply = currency_items[i].find_all('p')[5].text

    # writes data for each currency to results file
    f.write(f"#{i}:, {name}, {price}, {oneDayDeltaP}, {svnDayDeltaP}, {mCap}, {dayVol}, {cSupply}\n")

# closes the results file
f.close()