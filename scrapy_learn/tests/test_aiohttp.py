import asyncio
import aiohttp
import aiosqlite
import logging
import json

# async def fetch(_session, _url):
#     async with _session.get(_url) as response:
#         return await response.text(), response.status

# async def request():
#     url = 'http://httpbin.org/get'
#     async with aiohttp.ClientSession() as session:
#       html, status = await fetch(session, url)
#       print(f"status: {status}")
#       print(f"html: {html}")
      
# if __name__ == '__main__':
#     asyncio.run(request())
      
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s\n')

bookPerPage = 18
concurrency = 10

semaphore = asyncio.Semaphore(concurrency)
session = None

async def scrape_api(_url):
    async with semaphore:
      try:
        logging.info(f"scraping {_url}")
        async with session.get(_url) as response:
          return await response.json()
      except aiohttp.ClientError:
        logging.error(f"error occurred while scraping {_url}", exc_info=True)

async def scrape_index(_page):
    url = f"https://spa5.scrape.center/api/book/?limit={bookPerPage}&offset={bookPerPage * (_page - 1)}"
    return await scrape_api(url)
  
async def scrape():
    global session
    session = aiohttp.ClientSession()
    page = 503
    index_tasks = [asyncio.create_task(scrape_index(_page)) for _page in range(1, page + 1)]
    results = await asyncio.gather(*index_tasks)
    logging.info(f"results: {json.dumps(results, ensure_ascii=False, indent=2)}")
    await session.close()
    
if __name__ == '__main__':
    asyncio.run(scrape())