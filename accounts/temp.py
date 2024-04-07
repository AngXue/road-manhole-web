import requests

url = "http://localhost:8008/login.supported_modes"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers)

print(response.json())
