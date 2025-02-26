from flask import redirect, url_for, request, render_template
# from models import Movie
from forms import editMovieForm, searchMovieForm
import apirequest
from utils import clean_for_search_title, get_clean_description
from models import Book, db
import sqlalchemy


def edit():
    pass

def delete():
    pass

def get_volume_info(volume_id):
    response = apirequest.get_volume(volume_id)
    clean_description = get_clean_description(response['volumeInfo']['description'])
    
    try:
        imageLargeLink = response['volumeInfo']['imageLinks']['large']
        thumbnail = response['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        imageLargeLink = response['volumeInfo'].get('imageLinks', 'https://placehold.co/800x1200')
        thumbnail = response['volumeInfo'].get('imageLinks', 'https://placehold.co/139x203')

    data = {
        "volume_id": volume_id,
        "title": response['volumeInfo']['title'],
        "thumbnail" : thumbnail,
        "largeImage": imageLargeLink,
        "author": response['volumeInfo']['authors'][0], 
        "publishedDate": response['volumeInfo']['publishedDate'], 
        "description": clean_description,
        "publisher": response['volumeInfo']['publisher'], 
        "searchTitle": clean_for_search_title(response['volumeInfo']['title']),
    }
    try:
        volumeSeries = response['volumeInfo']['seriesInfo']['volumeSeries'][0]
        data['seriesId'] = volumeSeries['seriesId']
        data['seriesIndex'] = volumeSeries['orderNumber']
    except:
        data['seriesId'] = "Is not a Series"
        data['seriesIndex'] = 0
    # print(data)
    
    return data
def get_reading_badge(reading_status):
    reading_badge = "bg-"+ reading_status.replace(" ", "").lower()
    return reading_badge
    
def volume_info(volume_id):
    data = get_volume_info(volume_id)
    book_in_db = db.session.query(Book).filter_by(g_volume_id=volume_id).first()
    data_db = {}
    if book_in_db:
        data_db['series_id'] = book_in_db.series_id
        data_db['reading_status'] = book_in_db.reading_tag
        data_db['reading_badge'] = get_reading_badge(data_db['reading_status'])
    else:
        data_db['reading_status'] = "Not In Library"
        data_db['reading_badge'] = "bg-secondary"
        data_db['series_id'] = "Is not a Series"
    
    return render_template('volumeinfo.html', book=data, data_db=data_db)

def view_series(series_id):
    books = db.session.query(Book).filter_by(series_id=series_id).order_by(Book.series_index.asc()).all()
    return render_template('series.html', books=books)

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


def add(volume_id: str, shelf:str):
    data = get_volume_info(volume_id)
    # Create a new Book instance with the provided data
    # print(data)
    print(shelf)
    tags = ["To Read", "Currently Reading", "Completed"]
    if shelf not in tags:
        shelf = "Untagged"
    
    new_book = Book(
        title=data['title'],
        author=data['author'],
        publisher=data['publisher'],
        series_id=data['seriesId'],
        series_index=data['seriesIndex'],
        release_date=data['publishedDate'],
        description=data['description'],
        img_url=data['thumbnail'],  # Assuming 'thumbnail' holds the URL for the image
        reading_tag=shelf,
        g_volume_id=volume_id
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
    return render_template('temp.html')

def upcoming():
    return render_template('temp.html')
def home():
    
    # Get the minimum and maximum series index for each series ID
    # This is done by joining a subquery that groups by series ID and takes the minimum and maximum index
    # This ensures that we only get the first and last book in each series
    subquery = db.session.query(Book.series_id, 
                                sqlalchemy.func.min(Book.series_index).label('min_index'),
                                sqlalchemy.func.max(Book.series_index).label('max_index')).group_by(Book.series_id).subquery()
    
    reading_books = db.session.query(Book).filter(Book.reading_tag == "Currently Reading").all()
    
    to_read_books = db.session.query(Book).join(subquery, 
                                                (Book.series_id == subquery.c.series_id) & (Book.series_index == subquery.c.min_index)
                                    ).filter(Book.reading_tag == "To Read").all()
    completed_books = db.session.query(Book).join(subquery, 
                                                  (Book.series_id == subquery.c.series_id) & (Book.series_index == subquery.c.max_index)
                                      ).filter(Book.reading_tag == "Completed").all()
    
    all_books = {"Currently Reading": reading_books, "To read": to_read_books, "Completed": completed_books}
    return render_template('index.html', books = all_books)