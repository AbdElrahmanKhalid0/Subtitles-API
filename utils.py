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

def check_soup(soup):
    if "To many requests" in soup.prettify():
        print("Too many requests error")
        exit(1)