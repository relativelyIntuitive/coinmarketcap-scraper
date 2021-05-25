"# coinmarketcap-scraper" 

A simple scraping program I coded to pull market data for the top 100 currencies listed on the homepage of CoinMarketCap.com. The results will be saved to a SQLite database, as well a .CSV file created in the root directory.

1. Ensure that Python3 AND Chrome browser are properly installed on your system
2. Create a virtual environment within the root directory to install dependencies
3. Activate the virtual environment
3. With the venv active, run "pip install -r requirements.txt" command in the terminal at the root directory to install the dependencies
4. If on a Mac, modify line 10 of "scraper.py" to reference "chromedriver" without the ".exe"
5. The "chromedriver.exe" file is for the Windows edition of Chrome version 90, if you have a different version of chrome installed, download the proper driver from "https://chromedriver.chromium.org/downloads", unzip the package, and replace "chromedriver.exe" with the extracted executable
6. Run "scraper.py" with Python3 from the root directory
7. The program will run for less than 30 seconds, progress can be tracked in the terminal!
8. A .CSV file will be created within the root directory, containing the results!
9. The database will now contain the timestamped results! 

NO LICENSE! THIS CODE IS NOT MEANT TO BE REUSED OR REPRODUCED!
Copyright ©2021 Zachery A. Bielicki, all rights reserved