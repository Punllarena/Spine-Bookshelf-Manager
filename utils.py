import re

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