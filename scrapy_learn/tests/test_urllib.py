import urllib3

response = urllib3.request("GET", "http://www.python.org")
print(response.data)
print(type(response))

