import requests
import logging
import sqlite3

# url = "https://spa1.scrape.center/"
# html = requests.get(url).text
# print(html)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s\n')

scrape_limit = int(input("Please input the limit of perpage: "))
scrape_page = int(input("Please input the page number: "))

def scrape_api(url):
    logging.info(f"scraping {url}")
    try:
      res = requests.get(url)
      if res.status_code == 200:
        return res.json()
      logging.error(f"get invalid status code {res.status_code} while scraping {url}")
    except requests.RequestException:
      logging.error(f"error occurred while scraping {url}", exc_info=True)
      
def scrape_index(limit, page):
    url = f"https://spa1.scrape.center/api/movie/?limit={limit}&offset={limit * (page - 1)}"
    return scrape_api(url)
  
test_list = scrape_index(scrape_limit, scrape_page)
print(test_list)
