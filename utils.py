import webbrowser
from sys import argv

def put_results_in_web_page(html):
    """Takes an html string and puts it in a html file and opens it"""

    with open("page.html", "w", encoding="utf-8") as file:
        file.write(html)
    webbrowser.open("page.html")

def remove_dublicates(l):
    """removes dublicates in a list"""

    final_l = []
    for index ,item in enumerate(l):
        if l.index(item) == index:
            final_l.append(item)

    return final_l

def check_soup(soup, error: "the text that shows error in the page", error_msg: "the printed error message"):
    """checks the page if there was error in it like too many requests if the ip was panned"""

    if error in soup.prettify():
        print(error_msg)
        exit(1)

def ordinalText_to_int(text):
    """returns the int of a ordinal number, and returns false if the ordinal text
    was out of the function boundaries or it was invalid"""
    data = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10,
        "eleventh": 11,
        "twelfth": 12,
        "thirteenth": 13,
        "fourteenth": 14,
        "fifteenth": 15,
        "sixteenth": 16,
        "seventeenth": 17,
        "eighteenth": 18,
        "nineteenth": 19,
        "twentieth": 20,
        "twenty": 20,
        "thirtieth": 30,
        "thirty": 30,
        "fortieth": 40,
        "forty": 40,
        "fiftieth": 50,
        "fifty": 50,
        "sixtieth": 60,
        "sixty" : 60,
        "seventieth": 70,
        "seventy" : 70,
        "eightieth": 80,
        "eighty": 80,
        "ninetieth": 90,
        "ninety": 90,
        "hundredth": 100
    }

    text = text.lower()

    if text in data:
        return data[text]
    
    if len(text.split()) == 2:
        number = 0
        for ordinal_num in text.split():
            if ordinal_num in data:
                number += data[ordinal_num]
            else:
                return False
        return number
        
    elif len(text.split("-")) == 2:
        number = 0
        for ordinal_num in text.split("-"):
            if ordinal_num in data:
                number += data[ordinal_num]
            else:
                return False
        return number

    return False
