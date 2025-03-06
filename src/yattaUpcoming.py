from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from utils import clean_for_search_title

#Link to Yatta Tachi Resources. We're looking for the first link that points to the novel and manga releases for the month.
YATTA = "https://yattatachi.com/category/resources"

def tag_releases(title:str)->str: 
    if title.__contains__("Azuki") and title.__contains__("Chapter") or title.__contains__("NOOK Edition") and title.__contains__("#"):
        tag ="Individual Chapter Release"
        # print(f"[INFO] '{title}' is an Individual Chapter Release")
    elif title.__contains__("NOOK Edition"):
        tag = "NOOK Edition Release"
        # print(f"[INFO] '{title}' is a NOOK Edition Release")
    else: 
        tag = "None"
        # print(f"[INFO] '{title}' has no tags")
    return tag

def clean_for_search(title:str)->str:
    """
    Cleans a title string by removing certain punctuation characters.

    This function removes the following characters from the input title:
    colon (:), period (.), parentheses (()), ampersand (&), comma (,), and brackets ([]).
    
    Args:
        title (str): The title string to be cleaned.

    Returns:
        str: The cleaned title string with specified characters removed.
    """

    return title.translate(str.maketrans("","",":.()&,[]"))

def check_latest_post():
    try:
        print("[INFO] Opening Yatta Tachi Resources")
        request = requests.get(YATTA)
        request.raise_for_status()  # Raises an error for bad responses
        content = request.content
        soup = bs(content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An error occurred: {e}")


    latest_post = soup.find_all("li", class_="post-summary")

    print("[INFO] Checking for Manga / Light Novel / Books Releases post")
    for post in latest_post:
        print(post.text)
        if post.text.__contains__("Manga / Light Novel / Books Releases") or post.text.__contains__("Manga / Light Novel / Book Releases"):
            print("[INFO] Manga / Light Novel / Book Releases post Found:")
            book_release_post = post.text
            book_release_link = post.a["href"]
            print(f"[INFO] Title: {book_release_post}")
            print(f"[INFO] Link: {book_release_link}")
            break
    return book_release_link
    
def run_scraper(book_release_link = check_latest_post()):
    
    # book_release_link = check_latest_post()

    try:
        print(f"[INFO] Opening {book_release_link}")
        request = requests.get(book_release_link)
        request.raise_for_status()  # Raises an error for bad responses
        content = request.content
        releases_soup = bs(content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An error occurred: {e}")


    print("[INFO] Checking for Book Releases")

    book_releases = releases_soup.find_all("li", class_="release-single u-ta-c")
    book_info = {}



    for book in book_releases:
        # print(book)
        # Grab Release Date, format it to YYYY-MM-DD
        book_release_date = str(book).split("data-date=")[1].split(" ")[0].replace('"',"")
        date_string = book_release_date
        date_object = datetime.strptime(date_string, "%B-%d-%Y")
        formatted_date = date_object.strftime("%Y-%m-%d")
        # print(book_release_date)
        # print(formatted_date)
        book_img_link = str(book.find("div", class_="release-img")).split("url(")[1].split(")")[0]
        book_title = book.find("a", class_="release-link").text
        # print(f"[INFO] Processing Book Release {book_title}")
        book_tag = tag_releases(book_title)
        # book_release_link = book.find("a", class_="release-link").get("href")
        book_author = book.find("span", class_="release-author").text.split("By ")[1]
        book_release_type = book.find("span", class_="release-type").text
        book_release_company = book.find("span", class_="release-company").text
        book_info_dict = {
            # "Date": formatted_date,
            "Title": book_title.replace(":","-"),
            "Clean Search Title": clean_for_search_title(book_title),
            "Image Link": book_img_link,
            "Author": book_author,
            "Type": book_release_type,
            "Company": book_release_company,
            # "Link": book_release_link,
        }
        if book_tag == "None" and "Irodori" not in book_release_company:
            if formatted_date not in book_info:
                book_info[formatted_date] = []
            book_info[formatted_date].append(book_info_dict)
            
    return book_info

# data = run_scraper()
# import json
# with(open("./jsonresults/upcoming.json", "w")) as f:
#     json.dump(data, f)
