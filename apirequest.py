import requests
import os
from dotenv import load_dotenv

load_dotenv

api_key = os.getenv('BOOKS_API_KEY')

query = ""
volume_id = ""
startIndex = 0 # Starts at 0, counts each item in the list
maxResults = 10
params = {
    "q": query,
    "key": api_key,
    "startIndex": startIndex,
    "maxResults": maxResults, 
    "projection": "lite"
}

# Define your API key and base URL
search_url = f"https://www.googleapis.com/books/v1/volumes"


def next_page():
    pass

def search_volume(query, page=1):
    params['q'] = query
    params['startIndex'] = (page-1) * 10 # Starts at 0, counts each item in the list
    response = requests.get(search_url, params = params)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        pagination = data['totalItems']//maxResults
        data['pagination'] = pagination
        # print(data)
        return data
    else:
        print("Error:", response.status_code)
        return None
    
def get_volume(volume_id):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{volume_id}")
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None