import requests
import json

# MAKE AN API CALL, AND STORE THE RESPONSE
url = "https://hacker-news.firebaseio.com/v0/item/31353677.json"
r = requests.get(url)
print(f"Status Code: {r.status_code}")

# EXPLORE THE STRUCTURE OF THE DATA
response_dict = r.json()
response_string = json.dumps(response_dict, indent=4)
print(response_string)