import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key and base URL from environment variables
api_key = os.getenv('BOOKS_API_KEY')


# Define your API key and base URL

query = 'Chillin\' in Another World'
volume_id = "RkI3EAAAQBAJ"
search_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
volume_url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}?key={api_key}"

# Send the request to Google Books API
# response = requests.get(search_url)
response = requests.get(volume_url)
response.raise_for_status()

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data['volumeInfo']['seriesInfo']['volumeSeries'][0]['seriesId'])
    # for item in data['items']:
        # print(item['volumeInfo']['title'])
        # print(item['volumeInfo']['imageLinks']['thumbnail'])
        
else:
    print("Failed to retrieve data from Google Books API")
