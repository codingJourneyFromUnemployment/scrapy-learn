import requests
import logging

# url = "https://spa1.scrape.center/"
# html = requests.get(url).text
# print(html)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

index_url = f'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'