import asyncio
import aiohttp
import time



# async def get(_url):
#   return requests.get(_url)

# async def request():
#   url = "https://www.httpbin.org/delay/5"
#   print(f"waiting for {url}")
#   response =  await get(url)
#   print(f"get response from {url}, response: {response}")
  
# if __name__ == "__main__":
#   asyncio.run(request())

start = time.time()

async def get(_url):
  session = aiohttp.ClientSession()
  response = await session.get(_url)
  await session.close()
  return response

async def request():
  url = "https://www.httpbin.org/delay/5"
  print(f"waiting for {url}")
  response =  await get(url)
  print(f"get response from {url}, response: {response}")
  

tasks = [request() for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

end = time.time()
print(f"cost time: {end-start}")