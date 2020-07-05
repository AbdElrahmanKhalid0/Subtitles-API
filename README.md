<h1 align="center">
  <br>
  <img src="https://diymediahome.org/wp-content/uploads/Closed_Caption_Subtitles_logo.png">
  <br>
  Subtitle Api
  <br>
  <br>
</h1>

An unofficial api for subtitles from subscene, and also contains a script for getting subtitles from opensubtitle
using the library [python-opensubtitle](https://github.com/agonzalezro/python-opensubtitles).

## Install Dependencies

<code>pip install -r requirements.txt</code>

## Usage

To use the subscene api you can use it as a command line program like this

&nbsp; For Movies:

&nbsp;&nbsp; <code>python api.py -m MOVIE_NAME FORMAT LANGUAGE</code>

&nbsp; For Series Episode:

&nbsp;&nbsp; <code>python api.py -s SERIES_NAME FORMAT LANGUAGE SEASON_Number Episode_Number</code>

But in case you want to use it as a library there is two main functions in the api.py file you can use

&nbsp; The first one is <code>movie_subtitle</code> and can be used like this

```py
# "whiplash" is the title of the movie

# "english" is the subtitle language

# "bluray" is the format of the movie

# year is an optional argument that helps the script to choose precisely the movie if there was
# any similarity in names

# location is an optional argument to specify where the subtitles will be saved and when leaving
# it empty or not specifing it the subtitles will be saved in the current directory

# keep_zip_file is an optional argument default to False and it is used to determine if the downloaded
# zip file of the subtitle will be kept after downloading it or no

movie_subtitle("whiplash", "english", "bluray",
              year = "2014", location="path/to/save/subtitles/in",
              keep_zip_file=True)
```

&nbsp; The second one is <code>series_subtitle</code> and can be used like this

```py
# "westworld" is the title of the series
# 3 is the season number
# 1 is the episode number
# "english" is the subtitle language
# "webdl" is the format of the episode
# location and keep_zip_file are the same as in movie_subtitle
series_subtitle("westworld", 3, 1, "english", "webdl",
                location="path/to/save/subtitles/in", keep_zip_file=True)
```

the most of other functions in api.py are just helpers to scrape the pages and to download the subtitles.

## Licence

```
MIT License

Copyright (c) 2020 Abdelrahman Khalid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```