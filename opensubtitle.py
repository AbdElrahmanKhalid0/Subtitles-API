# the link to the git repository of the library
# https://github.com/agonzalezro/python-opensubtitles
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

ost = OpenSubtitles()
# the username and password of the opensubtitle account
ost.login("username", "password")

# the movie or episode path
f = File(r'path\to\file')


# you can get the subtitles Language Information with the function get_subtitle_language()
# ost.get_subtitle_languages()

# and then set the sublanguageid to the language id
data = ost.search_subtitles([{'sublanguageid': 'all', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])
id_subtitle_file = data[0].get('IDSubtitleFile')

# the output directory not set to any location so the subtitles will be downloaded in the
# current location
ost.download_subtitles([id_subtitle_file], output_directory='', extension='srt')


