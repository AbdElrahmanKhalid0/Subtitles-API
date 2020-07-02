import requests
import re
from bs4 import BeautifulSoup
from sys import argv, exit
from Errors import Errors
from utils import *

URL_SITE = "https://subscene.com"
URL_SEARCH_BY_TITLE = f"{URL_SITE}/subtitles/searchbytitle"

def get_args(argv: list):
    """gets the args and dictionarize them"""

    if len(argv) not in [3,5]:
        Errors.args_error()
    
    data = {}
    # getting the type of the title
    if "-" in argv[1]:
            data["type"] = "series" if argv[1] == "-s" else "movie"
    else:
        Errors.args_error()
    
    # getting the title itself
    data["title"] = argv[2]
    if data["type"] == "series":
        data["season"] = argv[3]
        data["episode"] = argv[4]
    
    return data


def get_matches(title: str, search_type: str = "all", backup_search_type: str = None) -> list:
    """gets the search matches of the specified title, and can specify the type
    of the given search so it can be ('exact', 'close', 'popular', or 'all') and
    'all' is the default option"""

    page = requests.post(URL_SEARCH_BY_TITLE, {"query": title})
    soup = BeautifulSoup(page.content, "html.parser")
    # check_soup(soup)
    
    # getting all the titles in the search page
    if search_type == "all":
        titles_subtitles_anchors = soup.find("div", class_="search-result").find_all("a")
    else:
        h2_search_type = soup.find("div", class_="search-result")\
            .find("h2", string=re.compile(search_type, re.IGNORECASE))
        
        if not h2_search_type:
            if backup_search_type:
                h2_search_type = soup.find("div", class_="search-result")\
                    .find("h2", string=re.compile(backup_search_type, re.IGNORECASE))
                if not h2_search_type:
                    return None
            else:
                return None
        
        titles_subtitles_anchors = h2_search_type.find_next("ul").find_all("a")  
            
    titles_subtitles_texts = remove_dublicates([anchor.text for anchor in titles_subtitles_anchors])
    titles_subtitles_links = [URL_SITE + anchor.get("href") for anchor in titles_subtitles_anchors]
    
    return dict(zip(titles_subtitles_texts, titles_subtitles_links))


def get_year(text: str) -> str:
    """gets the year of a title depending on its text"""
    
    if "(" not in text and ")" not in text:
        return None
    
    return text[text.find("(") + 1: text.find(")")]


def get_exact_match(title: str, year: str) -> str:
    """gets the exact match of a search query if it does exist and its page url"""
    
    matches = get_matches(title, search_type="exact", backup_search_type="close")
    
    if not matches:
        return None
    
    matches_by_year = [match for match in matches.keys() if get_year(match) == year]
    match = matches_by_year[0] if len(matches_by_year) else None

    url = matches[match]

    return match, url

def search_by_title(title: str) -> list:
    """gets the url to the title subtitle page, and returns None in case error happened"""
    
    # checking the type of the given title
    if type(title) != str:
        return None

    page = requests.post(URL_SEARCH_BY_TITLE, {"query": title})
    soup = BeautifulSoup(page.content, "html.parser")

    # all matches
    titles_subtitles_anchors = soup.find("div", class_="search-result").find_all("a")
    titles_subtitles_links = [URL_SITE + anchor.get("href") for anchor in titles_subtitles_anchors]
    
    print(remove_dublicates(titles_subtitles_links))
    # find


def main():
    title = get_args(argv)


if __name__ == "__main__":
    # main()
    # search_by_title("avengers")
    # print(get_matches("avengers", search_type="popular"))
    print(get_exact_match("avengers endgame", "2019"))
    # print(get_year("Avengers: Endgame (2019)"))