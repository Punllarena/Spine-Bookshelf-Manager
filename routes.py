from flask import redirect, url_for, request, render_template
# from models import Movie
from forms import editMovieForm, searchMovieForm
import apirequest
from utils import clean_for_search_title

def edit():
    pass

def delete():
    pass

def volume_info(volume_id):
    response = apirequest.get_volume(volume_id)
    clean_description = response['volumeInfo']['description'].replace("<p>", "").replace("</p>", "")    
    data = {
        "title": response['volumeInfo']['title'],
        "thumbnail" : response['volumeInfo']['imageLinks']['thumbnail'],
        "author": response['volumeInfo']['authors'][0], 
        "publishedDate": response['volumeInfo']['publishedDate'], 
        "description": clean_description,
        "publisher": response['volumeInfo']['publisher'], 
        "searchTitle": clean_for_search_title(response['volumeInfo']['title'])
    }
    # print(data)
    return render_template('volumeinfo.html', book=data)

def search(query, page):
    # print(f"Query:{query}")
    page = int(request.args.get('page', page))
    # print(f"Page:{page}")
    data = apirequest.search_volume(query, page)
    print(data)
    return render_template('search.html', books=data['items'], page=page, query=query, pagination=data['pagination'])

def add():
    pass

def home():
    return render_template('index.html')