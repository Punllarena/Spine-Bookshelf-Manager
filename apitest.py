import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key and base URL from environment variables
api_key = os.getenv('BOOKS_API_KEY')

# Define the query and pagination parameters
query = 'Chillin\' in Another World'
volume_id = "RkI3EAAAQBAJ"
startIndex = 9 # Starts at 0, counts each item in the list
maxResults = 10
params = {
    "q": query,
    "key": api_key,
    "startIndex": startIndex,
    "maxResults": maxResults
}


# Define your API key and base URL
search_url = f"https://www.googleapis.com/books/v1/volumes"
volume_url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"


# Send the request to Google Books API
response = requests.get(search_url, params = params)
response = requests.get(volume_url)
# response.raise_for_status()

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    seriesInfo = data['volumeInfo']['seriesInfo']['volumeSeries'][0]['seriesId']
    print(seriesInfo)
    # print(data)
    # print(data['volumeInfo']['seriesInfo']['volumeSeries'][0]['seriesId'])
    # for item in data['items']:
    #     print(item['volumeInfo']['title'])
        
        # print(item['volumeInfo']['imageLinks']['thumbnail'])
        
else:
    print("Failed to retrieve data from Google Books API")
