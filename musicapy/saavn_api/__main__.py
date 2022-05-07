from .api import SaavnAPI
from argparse import ArgumentParser
from pprint import pprint

# create parser
parser = ArgumentParser()

# add tags
# song services
parser.add_argument('-t', '--trending', dest='trending',
                    help='get trending songs', action='store_true')
parser.add_argument('-c', '--charts', dest='charts',
                    help='get charts', action='store_true')
parser.add_argument('-d', '--download', dest='download_links',
                    help='generate download links', action='store_true', default=True)
parser.add_argument('-l', '--link', dest='link',
                    help='link of song or album', type=str)

# album services
parser.add_argument('-aD', '--album-details',
                    dest='album_details', help='get album details from link', default=False, action='store_true')
parser.add_argument('-a', '--album', dest='album_download', help='get album download links',
                    default=False, action='store_true')

# search services
parser.add_argument('-sS', '--search-song', dest='search_song_query',
                    help='search song by name', type=str)
parser.add_argument('-sA', '--search-album', dest='search_album_query',
                    help='search album by name', type=str)
parser.add_argument('-sa', '--search-all', dest='search_all_query',
                    help='search album or song by name', type=str)


# parse args
args = parser.parse_args()

# extract args
link = args.link

search_song_query = args.search_song_query
search_album_query = args.search_album_query
search_all_query = args.search_all_query

trending = args.trending
charts = args.charts
download_link = args.download_links

album_details = args.album_details
album_download = args.album_download

# create api obj
api = SaavnAPI()

# create identifier if link is present
is_link = True if link else False
is_song = True if 'song/' in link else False
identifier = False
if is_link:
    identifier = api.create_identifier(link, 'song' if is_song else 'album')

# PERFORM ACTIONS #
# get trending songs
if trending:
    print("[TRENDING]")
    data = api.get_trending()
    pprint(data)

# get charts
if charts:
    print("[CHARTS]")
    data = api.get_charts()
    pprint(data)

# search song
if search_song_query:
    print("[SONGS SEARCH RESULT]")
    data = api.search_song(search_song_query)
    pprint(data)

# search album
if search_album_query:
    print("[ALBUMS SEARCH RESULT]")
    data = api.search_album(search_album_query)
    pprint(data)

# search all
if search_all_query:
    print("[SEARCH RESULT]")
    data = api.search_all(search_all_query)
    pprint(data)

# generate download links
if download_link and identifier and is_song:
    print("[SONG DOWNLOAD LINKS]")
    download_links = api.get_download_links(identifier)
    pprint(download_links)
elif not (trending or charts) and (trending or charts):
    print("[!] Cannot generate download links, song link not passed, use --help tag for more details")

# album details
if album_details and not is_song:
    print("[ALBUM DETAILS]")
    details = api.get_album_details(identifier)
    pprint(details)
elif album_details and is_song:
    print("[!] Album Link is Invalid")

# generate album download links
if album_download and not is_song:
    print("[ALBUM DOWNLOAD LINKS]")
    data = api.generate_album_download_links(identifier) 
    pprint(data)
elif album_download and is_song:
     print("[!] Album Link is Invalid")