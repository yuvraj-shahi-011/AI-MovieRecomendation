import requests

API_KEY = "3a812058"

url = f"https://www.omdbapi.com/?apikey={API_KEY}&t=Interstellar"

response = requests.get(url)

print(response.json())