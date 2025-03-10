import re
import os
from models import Book, db
from datetime import datetime

def restore_backup(file):
    print("[INFO] Restoring Backup")
    with open(file, "r") as f:
        print("[INFO] Reading Backup")
        if not file.endswith('.csv'):
            os.remove(file)
            print("[ERROR] Invalid file format")
            return "[ERROR] Invalid file format"
        for line in f.readlines():
            if line.startswith("#"):
                continue
            data = line.strip().split(";")
            book = db.session.query(Book).filter_by(g_volume_id=data[10]).first()
            print("[INFO] Restoring Book:" + data[0])
            if book is not None:
                print("[INFO] Book already exists, rolling back")
                db.session.rollback()
                continue
            if data[16] == "No Data":
                data[16] = datetime.now().strftime("%Y-%m-%d")
            if data[15] == "No Data":
                data[15] = datetime.now().strftime("%Y-%m-%d")
            book = Book(
                title=data[0],
                author=data[1],
                series_id=data[2],
                series_index=data[3],
                reading_tag=data[4],
                release_date=data[5],
                description=data[6],
                rating=data[7],
                review=data[8],
                img_url=data[9],
                g_volume_id=data[10],
                start_date=data[11],
                finish_date=data[12],
                hour_read=data[13],
                minutes_read=data[14],
                created_at=data[15],
                last_updated=data[16]
            )
            db.session.add(book)
            db.session.commit()
    return "Restoration Complete"
def download_backup():
    
    backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backup.csv')
    with open(backup_path, "w") as f:
        f.write("#title;author;series_id;series_index;reading_tag;release_date;description;rating;review;img_url;g_volume_id;start_date;finish_date;hour_read;minutes_read;created_at;last_updated\n")
    
        for book in db.session.query(Book).all():
            created_at = getattr(book, 'created_at', 'No Data')
            last_updated = getattr(book, 'last_updated', 'No Data')
            
            # Clean and format fields to remove unnecessary whitespace
            fields = [
                book.title.strip() if book.title else 'No Data',
                book.author.strip() if book.author else 'No Data',
                str(book.series_id).strip() if book.series_id else 'No Data',
                str(book.series_index).strip() if book.series_index else 'No Data',
                book.reading_tag.strip() if book.reading_tag else 'No Data',
                str(book.release_date).strip() if book.release_date else 'No Data',
                book.description.strip() if book.description else 'No Data',
                str(book.rating).strip() if book.rating else 'No Data',
                book.review.strip() if book.review else 'No Data',
                book.img_url.strip() if book.img_url else 'No Data',
                book.g_volume_id.strip() if book.g_volume_id else 'No Data',
                str(book.start_date).strip() if book.start_date else 'No Data',
                str(book.finish_date).strip() if book.finish_date else 'No Data',
                str(book.hour_read).strip() if book.hour_read else 'No Data',
                str(book.minutes_read).strip() if book.minutes_read else 'No Data',
                str(created_at).strip(),
                str(last_updated).strip()
            ]
            
            f.write(";".join(fields) + "\n")

        return backup_path
    

def clean_for_search_title(title):
    replacements = {
        ":": "",
        ",": "",
        ".": "",
        "-": " ",
        "?":"",
        "!":"",
        "(volume)": "",
        "Volume": "",
        "volume": "",
        "vol": "",
        "Vol":"",
        "act": "",
        "(manga)": "", 
        "manga": "",
        "Manga": "",
        "(light novel)": "",
        "Light Novel":"",
        "(":"",
        ")":"",
        "()":"",
        "Hardcover":"",
        " ":"+",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title

def get_clean_description(description):
    
    replace_text = {
        "<p>": "",
        "</p>": "",
        "<br>": "",
        "</br>": "",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&apos;": "'",
        "&nbsp;": " ",
        "<b>":"",
        "</b>":"",
        "<i>":"",
        "</i>":"",
        "<strong>":"",
        "</strong>":"",
        "<em>":"",
        "</em>":"",
        "<u>":"",
        "</u>":"",
        "<span>":"",
        "</span>":"",
        "<sup>":"",
        "</sup>":"",
        "<sub>":"",
        "</sub>":"",
        "<sup>":"",
        "</sup>":"",
    }

    for key, value in replace_text.items():
        description = description.replace(key, value)
    
    return description