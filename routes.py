from flask import redirect, url_for, request, render_template
# from models import Movie
from forms import editMovieForm, searchMovieForm
import apirequest
from utils import clean_for_search_title
from models import Book, db
import sqlalchemy


def edit():
    pass

def delete():
    pass

def get_volume_info(volume_id):
    response = apirequest.get_volume(volume_id)
    clean_description = response['volumeInfo']['description'].replace("<p>", "").replace("</p>", "")    
    
    try:
        imageLargeLink = response['volumeInfo']['imageLinks']['large']
    except KeyError:
        imageLargeLink = response['volumeInfo']['imageLinks']['thumbnail']
    data = {
        "volume_id": volume_id,
        "title": response['volumeInfo']['title'],
        "thumbnail" : response['volumeInfo']['imageLinks']['thumbnail'],
        "largeImage": imageLargeLink,
        "author": response['volumeInfo']['authors'][0], 
        "publishedDate": response['volumeInfo']['publishedDate'], 
        "description": clean_description,
        "publisher": response['volumeInfo']['publisher'], 
        "searchTitle": clean_for_search_title(response['volumeInfo']['title']),
        "ISBN10": response['volumeInfo']['industryIdentifiers'][0]['identifier'],
        "ISBN13": response['volumeInfo']['industryIdentifiers'][1]['identifier'],
    }
    try:
        volumeSeries = response['volumeInfo']['seriesInfo']['volumeSeries'][0]
        data['seriesId'] = volumeSeries['seriesId']
        data['seriesIndex'] = volumeSeries['orderNumber']
    except:
        data['seriesID'] = "Is not a Series"
        data['seriesIndex'] = 0
    # print(data)

    return data
    
def volume_info(volume_id):
    data = get_volume_info(volume_id)
    # print(data)
    return render_template('volumeinfo.html', book=data)

def search(page=1):
    if request.method == 'POST':
        query = request.form['query']
        page = int(request.args.get('page', page))
        data = apirequest.search_volume(query, page)
        try: 
            books = data['items']
        except:
            books = "No Results"
    return render_template('search.html',
                        books=books, 
                        searchQuery=query, 
                        pagination=data['pagination'], 
                        page=page)


def add(volume_id):
    data = get_volume_info(volume_id)
    # Create a new Book instance with the provided data
    print(data)
    
    
    new_book = Book(
        title=data['title'],
        author=data['author'],
        publisher=data['publisher'],
        seriesID=data['seriesId'],
        seriesIndex=data['seriesIndex'],
        release_date=data['publishedDate'],
        description=data['description'],
        img_url=data['thumbnail']  # Assuming 'thumbnail' holds the URL for the image
    )
    # Add the new book to the database session and commit
    try:
        db.session.add(new_book)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return '''
    <script>
    window.close();
    </script>
    '''


def guide():
    return render_template('index.html')

def upcoming():
    return render_template('index.html')
def home():
    return render_template('index.html')