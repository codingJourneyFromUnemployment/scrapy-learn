import requests
import logging
import sqlite3
from colorama import Fore, Back, Style

# url = "https://spa1.scrape.center/"
# html = requests.get(url).text
# print(html)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s\n')

# scrape_limit = int(input("Please input the limit of perpage: "))
# scrape_page = int(input("Please input the page number: "))

# def scrape_api(url):
#     logging.info(f"scraping {url}")
#     try:
#       res = requests.get(url)
#       if res.status_code == 200:
#         return res.json()
#       logging.error(f"get invalid status code {res.status_code} while scraping {url}")
#     except requests.RequestException:
#       logging.error(f"error occurred while scraping {url}", exc_info=True)
      
# def scrape_index(limit, page):
#     url = f"https://spa1.scrape.center/api/movie/?limit={limit}&offset={limit * (page - 1)}"
#     return scrape_api(url)
  
# test_list = scrape_index(scrape_limit, scrape_page)
# print(test_list)

number = int(input(Fore.GREEN + "Please input the number of the movie: \n" + Style.RESET_ALL))
movie_dict = {}

con = sqlite3.connect("movie.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movie (title, score)")

def scrape_detail(number):
    logging.info(f"scraping detail of {number}")
    try:
      for i in range(1, number + 1):
        url = f"https://spa1.scrape.center/api/movie/{i}"
        res = requests.get(url)
        if res.status_code == 200:
          movie_dict[i] = res.json()
        else:
          logging.error(f"get invalid status code {res.status_code} while scraping {url}")
        
      return movie_dict
    
    except requests.RequestException:
      logging.error(f"error occurred while scraping {url}", exc_info=True)
      
def save_to_db(movie_dict):
    for key in movie_dict.keys():
      title = movie_dict[key]["name"]
      score = movie_dict[key]["score"]
      cur.execute("INSERT INTO movie (title, score) VALUES (?, ?)", (title, score))
      con.commit()
      logging.info(f"inserted {title} into database")
      
def query_db():
    cur.execute("SELECT * FROM movie")
    for row in cur.fetchall():
      print(row)
      
def main():
    try :
      movie_dict = scrape_detail(number)
      save_to_db(movie_dict)
      query_db()
    except Exception as e:
      print(Fore.RED + "Error: ", e, Style.RESET_ALL)
      
      
if __name__ == "__main__":
    query_db()
        