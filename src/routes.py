from flask import request, render_template, redirect, url_for, send_file, after_this_request
# from forms import editMovieForm, searchMovieForm
import apirequest
from utils import clean_for_search_title, get_clean_description, download_backup, restore_backup
from models import Book, Upcoming, db
import sqlalchemy
from forms import UploadBackupForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename
import os

def settings():
    message = "None"
    form = UploadBackupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src','static', 'upload')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src','static', 'upload', filename)
            f.save(save_path)
            message = restore_backup(save_path)
            # message = "Backup restored successfully"
            os.remove(save_path)
            return redirect(url_for('settings'))
    if request.args.get('action') == 'download_backup':
        print("[INFO] Downloading Backup")
        file_path = download_backup()
        @after_this_request
        def remove_file(response):
            try:
                print(f"Deleting file: {file_path}")
                os.remove(file_path)
            except OSError as e:
                print(f"Error deleting file: {e}")
            return response
        message = "Backup downloaded successfully"
        return send_file(file_path, as_attachment=True)
    return render_template('settings.html', form=form, message=message)

def edit(volume_id):
    book_in_db = db.session.query(Book).filter_by(g_volume_id=volume_id).first()
    if request.method == 'POST':
        response = request.form.to_dict()
        if book_in_db:
            for key, value in response.items():
                setattr(book_in_db, key, value)
            book_in_db.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # TODO Remove comment once Backup and Restore has been implemented
            if response['reading_tag'] == "Completed" and not book_in_db.finish_date:
                book_in_db.finish_date = datetime.now().strftime("%Y-%m-%d")
            if response['reading_tag'] == "Currently Reading" and not book_in_db.start_date:
                book_in_db.start_date = datetime.now().strftime("%Y-%m-%d")
            db.session.commit()
        return redirect(url_for('volume_info', volume_id = volume_id))
    elif book_in_db:
        return render_template('edit.html', book=book_in_db)
    else:
        return render_template('404.html'), 404

def delete(volume_id):
    book_in_db = db.session.query(Book).filter_by(g_volume_id=volume_id).first()
    if book_in_db:
        db.session.delete(book_in_db)
        db.session.commit()
    return redirect(url_for('volume_info', volume_id = volume_id))

def get_volume_info(volume_id):
    book = apirequest.get_volume(volume_id)

    # Image (thumbnail and large are the same in RanobeDB)
    image = book.get('image')
    if image and image.get('filename'):
        image_url = f"https://images.ranobedb.org/{image['filename']}"
    else:
        image_url = 'https://placehold.co/139x203'

    # Author: from original edition (eid=0 / lang=null), prefer romaji
    author = "Unknown"
    for edition in book.get('editions', []):
        if edition.get('eid') == 0 or edition.get('lang') is None:
            for staff in edition.get('staff', []):
                if staff['role_type'] == 'author':
                    author = staff.get('romaji') or staff['name']
                    break
            break

    # Publisher: prefer EN publisher, fallback to first
    publisher = "Unknown"
    for p in book.get('publishers', []):
        if p.get('lang') == 'en' and p.get('publisher_type') == 'publisher':
            publisher = p['name']
            break
    if publisher == "Unknown" and book.get('publishers'):
        publisher = book['publishers'][0]['name']

    # Release date: prefer EN, convert YYYYMMDD int to "YYYY-MM-DD"
    raw_date = book.get('c_release_dates', {}).get('en') or book.get('c_release_date')
    if raw_date:
        s = str(raw_date)
        publishedDate = f"{s[:4]}-{s[4:6]}-{s[6:]}"
    else:
        publishedDate = "Unknown"

    clean_description = get_clean_description(book.get('description', ''))

    # Series info
    series_info = book.get('series')
    if series_info and series_info.get('id'):
        series_id = series_info['id']
        series_data = apirequest.get_series(series_id)
        series_index = 0
        for b in series_data.get('books', []):
            if b['id'] == int(volume_id):
                series_index = b.get('sort_order', 0)
                break
    else:
        series_id = "Is not a Series"
        series_index = 0

    return {
        "volume_id": volume_id,
        "title": book['title'],
        "thumbnail": image_url,
        "largeImage": image_url,
        "author": author,
        "publishedDate": publishedDate,
        "description": clean_description,
        "publisher": publisher,
        "searchTitle": clean_for_search_title(book['title']),
        "seriesId": series_id,
        "seriesIndex": series_index,
    }
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
        data_db['hour_read'] = book_in_db.hour_read
        data_db['minutes_read'] = book_in_db.minutes_read
        data_db['start_date'] = book_in_db.start_date
        data_db['finish_date'] = book_in_db.finish_date
        data_db['rating'] = book_in_db.rating
        data_db['review'] = book_in_db.review
    else:
        data_db['reading_status'] = "Not In Library"
        data_db['reading_badge'] = "bg-secondary"
        data_db['series_id'] = "Is not a Series"
        data_db['hour_read'] = "No Data"
        data_db['minutes_read'] = "No Data"
        data_db['start_date'] = "No Data"
        data_db['finish_date'] = "No Data"
        data_db['rating'] = "No Data"
        data_db['review'] = "No Data"
        
    
    return render_template('volumeinfo.html', book=data, data_db=data_db)

def view_series(series_id):
    """
    Renders a template displaying books in a series.

    Args:
        series_id (str): The ID of the series whose books are to be displayed.

    Returns:
        str: Rendered HTML of the series page with the books ordered by series index.
    """

    books = db.session.query(Book).filter_by(series_id=series_id).order_by(Book.series_index.asc()).all()
    return render_template('series.html', books=books)

def search(page=1):
    if request.method == 'POST':
        query = request.form['query']
        if not query:
            query = "Book Spine"
        page = int(request.args.get('page', page))
        data = apirequest.search_volume(query, page)
        books = data.get('books') or "No Results"
    return render_template('search.html',
                        books=books, 
                        searchQuery=query, 
                        pagination=data['pagination'], 
                        page=page)


def add(volume_id: str, shelf:str):
    data = get_volume_info(volume_id)
    # Create a new Book instance with the provided data
    # print(data)
    # print(shelf)
    tags = ["To Read", "Currently Reading", "Completed"]
    if shelf not in tags:
        shelf = "To Read"
    
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
        g_volume_id=volume_id,
        review = "No Data",
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
    )
    if shelf == "Completed":
        new_book.finish_date = datetime.now().strftime("%Y-%m-%d")
    if shelf == "Currently Reading":
        new_book.start_date = datetime.now().strftime("%Y-%m-%d")
    # Add the new book to the database session and commit
    try:
        db.session.add(new_book)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
    return redirect(url_for('volume_info', volume_id=volume_id))

def timeline(year_month = datetime.now().strftime("%Y-%m")):
    year_month = request.args.get("year_month", year_month)
    db_data = db.session.query(Book).filter(Book.finish_date.startswith(year_month)).order_by(Book.finish_date.asc()).all()
    display_month = datetime.strptime(year_month, "%Y-%m").strftime("%B %Y") 
    #example: "January 2023"
    return render_template('timeline.html', books=db_data, display=display_month)
    

def upcoming():
    year_month = request.args.get("year_month", datetime.now().strftime("%Y-%m"))
    current = datetime.strptime(year_month, "%Y-%m")
    prev_month = (current - relativedelta(months=1)).strftime("%Y-%m")
    next_month = (current + relativedelta(months=1)).strftime("%Y-%m")
    display_month = current.strftime("%B %Y")

    cache_key = f"ranobedb:{year_month}"
    db_data = db.session.query(Upcoming).filter_by(release_link=cache_key).first()

    if db_data:
        releases = db_data.data_dict
    else:
        releases = apirequest.get_releases(year_month)
        db.session.add(Upcoming(release_link=cache_key, data_dict=releases))
        db.session.commit()

    releases_by_date = {}
    for r in releases:
        date = r.get("release_date_str", "Unknown")
        releases_by_date.setdefault(date, []).append(r)

    return render_template('upcoming.html',
                           books=releases_by_date,
                           display_month=display_month,
                           year_month=year_month,
                           prev_month=prev_month,
                           next_month=next_month)

def full_shelf(page_num):
    query = db.session.query(Book).order_by(Book.series_id, Book.series_index).paginate(per_page = 20 ,page = page_num, error_out = True)
    total_items = db.session.query(Book).count()
    return render_template('fullshelf.html', books=query, total_items=total_items)

def shelf(page_num, tag):
    if tag not in ["To Read", "Currently Reading", "Completed"]:
        tag = "To Read"
    shelf = db.session.query(Book).filter(Book.reading_tag == tag).order_by(Book.series_id, Book.series_index).paginate(per_page = 20 ,page = page_num, error_out = True)
    total_items = db.session.query(Book).filter(Book.reading_tag == tag).count()
    return render_template('shelf.html', books=shelf, tag=tag, total_items=total_items)

def home():
    
    # Get the minimum and maximum series index for each series ID
    # This is done by joining a subquery that groups by series ID and takes the minimum and maximum index
    # This ensures that we only get the first and last book in each series
    subquery = db.session.query(Book.series_id, 
                                sqlalchemy.func.min(Book.series_index).label('min_index'),
                                sqlalchemy.func.max(Book.series_index).label('max_index')).group_by(Book.series_id).subquery()
    
    reading_books = db.session.query(Book).filter(Book.reading_tag == "Currently Reading").order_by(Book.last_updated.desc()).all()
    
    to_read_books = db.session.query(Book).outerjoin(subquery, 
                                                    (Book.series_id == subquery.c.series_id) & (Book.series_index == subquery.c.min_index)
                                        ).filter(
                                            (subquery.c.min_index == None) | 
                                            (Book.series_index == subquery.c.min_index)
                                        ).filter(Book.reading_tag == "To Read").order_by(Book.last_updated.desc()).limit(4).all()
    completed_books = db.session.query(Book).outerjoin(subquery, 
                                                    (Book.series_id == subquery.c.series_id) & (Book.series_index == subquery.c.max_index)
                                        ).filter(
                                            (subquery.c.max_index == None) | 
                                            (Book.series_index == subquery.c.max_index)
                                        ).filter(Book.reading_tag == "Completed").order_by(Book.last_updated.desc()).limit(4).all()
    
    all_books = {"Currently Reading": reading_books, "To read": to_read_books, "Completed": completed_books}
    return render_template('index.html', books = all_books)