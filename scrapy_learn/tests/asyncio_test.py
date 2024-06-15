import asyncio
import requests

async def request():
  url = "https://www.httpbin.org/delay/5"
  print(f"waiting for {url}")
  response =  await requests.get(url)
  print(f"get response from {url}, response: {response}")
  
if __name__ == "__main__":
  asyncio.run(request())
