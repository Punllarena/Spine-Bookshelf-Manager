import re

def clean_for_search_title(title):
    replacements = {
        ":": "",
        ",": "",
        ".": "",
        "-": "  ",
        "(volume)": "",
        "Volume": "",
        "volume": "",
        "vol": "",
        "Vol":"",
        "act": "",
        "(manga)": "", 
        "manga": "",
        "(light novel)": "",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title