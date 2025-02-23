import re

def clean_for_search_title(title):
    replacements = {
        ":": "",
        "(volume)": "",
        "volume": "",
        "vol": "",
        "act": "",
        "(manga)": "", 
        "manga": "",
        "(light novel)": "",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title