# jsonRest.py
import requests


def fetch_json_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns JSON response as a dictionary
    else:
        return {"error": "Failed to retrieve data"}
