import requests

BASE_URL = "https://ranobedb.org/api/v0"

query = "Chillin' in Another World with Level 2 Super Cheat Powers"
book_id = 12020  # Mushoku Tensei Vol. 1

# Test search
search_response = requests.get(f"{BASE_URL}/books", params={"q": query, "rl": "en", "limit": 10, "page": 1})
if search_response.status_code == 200:
    data = search_response.json()
    print("Search results:")
    for book in data.get("books", []):
        print(f"  [{book['id']}] {book['title']}")
    print(f"  Total pages: {data.get('totalPages')}")
else:
    print("Search failed:", search_response.status_code)

# Test book detail
book_response = requests.get(f"{BASE_URL}/book/{book_id}")
if book_response.status_code == 200:
    book = book_response.json()["book"]
    print(f"\nBook detail for id={book_id}:")
    print(f"  Title: {book['title']}")
    print(f"  Series id: {book.get('series', {}).get('id')}")
else:
    print("Book detail failed:", book_response.status_code)
