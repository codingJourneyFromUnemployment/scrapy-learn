# from selenium import webdriver

# browser = webdriver.Chrome()  
# browser.get('http://www.google.com/')
# print(browser.page_source)

# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common import by

# browser = webdriver.Chrome()
# browser.get('http://www.taobao.com')
# waitInstance = WebDriverWait(browser, 10)
# input = waitInstance.until(EC.presence_of_element_located((by.By.ID, 'a')))
# button = waitInstance.until(EC.element_to_be_clickable((by.By.CSS_SELECTOR, '.btn-search')))
# print(input, button)

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# chrome_option = Options()
# chrome_option.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_option)
# browser.get('http://www.baidu.com')
# browser.get_screenshot_as_file('baidu.png')


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
import sqlite3
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s\n')

time_out = 10
total_page = 10
detailPageUrlList = []
movieDetailList = []

con = sqlite3.connect("movie.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movie (url, name, categories, cover, score, drama)")

browser = webdriver.Chrome()
waitInstance = WebDriverWait(browser, time_out)

def scrape_page(url, condition, locator):
  logging.info(f"scraping {url}")
  try:
    browser.get(url)
    waitInstance.until(condition(locator))
  except TimeoutException:
    logging.error(f"error occurred while scraping {url}", exc_info=True)
    
def scrape_index(page):
  url = f"https://spa2.scrape.center/page/{page}"
  scrape_page(url,
              condition=EC.visibility_of_all_elements_located,
              locator=(By.CSS_SELECTOR, '#index .item'))
  
def parse_index():
  base_url = 'https://spa2.scrape.center/'
  elements = browser.find_elements(By.CSS_SELECTOR, '#index .item .name')
  for element in elements:
    href = element.get_attribute('href')
    detailPageUrl = urljoin(base_url, href)
    detailPageUrlList.append(detailPageUrl)
    logging.info(f"detailPageUrl: {detailPageUrl}")
    
def scrape_detail(url):
  scrape_page(url,
              condition=EC.visibility_of_element_located,
              locator=(By.TAG_NAME, 'h2'))

def parse_detail():
  url = browser.current_url
  name = browser.find_element(By.TAG_NAME, 'h2').text
  categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
  cover = browser.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
  score = browser.find_element(By.CLASS_NAME, 'score').text
  drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text
  return {
    'url': url,
    'name': name,
    'categories': categories,
    'cover': cover,
    'score': score,
    'drama': drama
  }
  
def save_to_db(movieDetailList):
  for movie in movieDetailList:
    cur.execute("INSERT INTO movie (url, name, categories, cover, score, drama) VALUES (?, ?, ?, ?, ?, ?)",
                (movie['url'], movie['name'], str(movie['categories']), movie['cover'], movie['score'], movie['drama']))
    logging.info(f"database added: {movie['name']}")
  con.commit()
    
def query_db():
  con = sqlite3.connect("movie.db")
  cur = con.cursor()
  movie = input("Please input the name of the movie: ")
  cur.execute("SELECT * FROM movie WHERE name=?", (movie,))
  for row in cur.fetchall():
    print(row)
    
def main():
  try:
    for page in range(1, total_page + 1):
      scrape_index(page)
      parse_index()
      
    for detailPageUrl in detailPageUrlList:
      scrape_detail(detailPageUrl)
      detail = parse_detail()
      movieDetailList.append(detail)
      
    save_to_db(movieDetailList)
    
  except Exception:
    logging.error('error occurred while scraping', exc_info=True)
  finally:
    browser.close()
    
# main()

query_db()
    

    
    





