import requests
import re
import os
import zipfile
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
    check_soup(soup, "To many requests", "Too many requests error")
    
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
            
    titles_subtitles_texts = remove_dublicates([anchor.text.strip() for anchor in titles_subtitles_anchors])
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


class Subtitle:
    def __init__(self, htmlNode):
        self.setAttrs(htmlNode)

    def setAttrs(self, htmlNode):
        self.link = URL_SITE + htmlNode.find("td", class_="a1").find("a")["href"]
        self.language = htmlNode.select("span.l.r")[0].text.strip()
        self.title = htmlNode.find_all("span")[1].text.strip()
        self.format = self.get_subtitle_format(self.title)

    @staticmethod
    def get_subtitle_format(sub_title):
        """gets the format of the subtitle (bluray, hdrip, web-dl, trailer, ...)
        and returns None in case of unknown type"""
        
        # the following RegEx are for finding the blueray or the blue-ray
        if "trailer" in sub_title.lower():
            return "trailer"
        elif re.compile(".*blu?[\s\S]ray.*").match(sub_title.lower()):
            return "bluray"
        elif re.compile(".*hd?[\s\S]rip.*").match(sub_title.lower()):
            return "hdrip"
        elif re.compile(".*web?[\s\S]dl.*").match(sub_title.lower()):
            return "web-dl"
        elif re.compile(".*hd?[\s\S]ts.*").match(sub_title.lower()):
            return "hd-ts"
        elif re.compile(".*hd?[\s\S]tc.*").match(sub_title.lower()):
            return "hd-tc"
        elif re.compile(".*web?[\s\S]rip.*").match(sub_title.lower()):
            return "webrip"
        elif re.compile(".*br?[\s\S]rip.*").match(sub_title.lower()):
            return "brrip"
        elif re.compile(".*bd?[\s\S]rip.*").match(sub_title.lower()):
            return "bdrip"
        else:
            return None
        

def get_subtitles(title_page_url: str, languages: list = ['en']) -> list:
    """gets the subtitles from a specific title page"""

    page = requests.get(title_page_url)
    soup = BeautifulSoup(page.content, "html.parser")
    check_soup(soup, "To many requests", "Too many requests error")

    # getting the subtitles nodes and then removing the empty ones from it
    subtitles_nodes = soup.find("div", class_="content clearfix")\
        .find("table").find("tbody").find_all("tr")
    subtitles_nodes = [subtitle_node for subtitle_node in subtitles_nodes if subtitle_node.find("a")]
    
    subtitles = [Subtitle(subtitle_node) for subtitle_node in subtitles_nodes]

    return subtitles
    

def get_subtitle(subtitile: Subtitle, location: str = "", keep_zip_file: bool = False):
    """gets the subtitle itself and saves it to a specific location,
    and returns True in case of succession"""

    # write to the current location if there was no specified location
    # if there was a one write to it
    if location:
        try:
            os.chdir(location)
        except:
            Errors.location_error()

    page = requests.get(subtitile.link)
    soup = BeautifulSoup(page.content, "html.parser")

    download_link = URL_SITE + soup.find("a", {"id":"downloadButton"})["href"]

    # getting the file and writing it to the disk
    subtitle_zip_file = requests.get(download_link, allow_redirects=True)
    with open(subtitile.title + ".zip", "wb") as file:
        file.write(subtitle_zip_file.content)
    
    # unzipping the subtitle zip file and putting the subtitles in a file with the same name
    # as the subtitle title and the zip file name
    with zipfile.ZipFile(subtitile.title + ".zip", "r") as zip_file:
        zip_file.extractall(subtitile.title)
    
    # removing the old zip file
    if not keep_zip_file:
        os.remove(subtitile.title + ".zip")

    return True


def movie_subtitle(title: str, year: str, language: str, format: "format of movie (bluray, hdrip...)", location: str = "", keep_zip_file: bool = False):
    """downloads a movie subtitle and saves it to the current location or to a
    specified location, and returns True in case of succession and False in case
    of problem existance"""

    subtitles = get_subtitles(get_exact_match(title, year)[1])
    subtitle = [subtitle for subtitle in subtitles if subtitle.language.lower() == language and subtitle.format == Subtitle.get_subtitle_format(format)]
    
    # in case there wasn't any subtitle with the given information it will return False
    # but if there was it will assign the subtitle to the first subtitle that matches
    # the given information
    if not subtitle:
        print("Couldn't get any subtitle with the given information")
        return False
    else:
        subtitle = subtitle[0]
    
    if get_subtitle(subtitle, location, keep_zip_file):
        print("saved the subtitle successfully.")
        return True
    else:
        return False


def get_matches_series(title: str, specific_sub_title: str = "") -> list:
    """gets the links of the subtitles of all the seasons of a series
    or gets a specific version (specific title of the series)"""

    all_matches = get_matches(title, "tv-series")
    # the "{title} - SEASON" is the format that subscene follows in series titles
    if not specific_sub_title:
        matches = [{match: all_matches[match]} for match in all_matches.keys() if f"{title} - " in match.lower() and "season" in match.lower()]
    else:
        matches = [{match: all_matches[match]} for match in all_matches.keys() if f"{title} - {specific_sub_title}" in match.lower()]
    
    return matches


def get_series_season(title: str, season: int) -> dict:
    """gets a season of a series subtitles page link"""

    matches = get_matches_series(title)
    for match in matches:
        key = list(match.keys())[0]
        # getting the season ordinal number only
        ordinal_season_number = key.lower().replace(f"{title.lower()} - ","").replace(" season","")
        if season == ordinalText_to_int(ordinal_season_number):
            return match
    
    return False



def main():
    title = get_args(argv)


if __name__ == "__main__":
    # movie_subtitle("whiplash", "2014", "english", "bdrip")
    # print(get_matches_series("westworld"))
    print(get_series_season("westworld", 3))
    # print(ordinalText_to_int("eighth"))
    # main()
    # print(get_matches("avengers", search_type="popular"))
    # print(get_exact_match("avengers endgame", "2019"))
    # subtitles = get_subtitles(get_exact_match("avengers endgame", "2019")[1])
    # subtitle = [subtitle for subtitle in subtitles if subtitle.format == "bluray"][0]
    # get_subtitle(subtitle)
    # print(get_year("Avengers: Endgame (2019)"))