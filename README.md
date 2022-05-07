# MusicAPy

Music API Python wrapper, currently supports limited API.

- Supported API
  - JioSaavn

## Installation

- Using pip and git

    ```bash
    python3 -m pip install git+https://github.com/dmdhrumilmistry/MusicAPy
    ```

- Using pypi

    ```bash
    python3 -m pip install MusicAPy
    ```

## Usage

- Jio Saavn API

  - From Script

    ```python
    from musicapy.saavn_api import SaavnAPI
    
    # create API obj
    api = SaavnAPI()
    
    
    ## Search Services
    # Search Song
    data = api.search_song('song_name')

    # Search Album
    data = api.search_album('album_name')

    # Search All
    data = api.search_all('song_or_album_name')

    ## Song Services
    # get song link
    saavn_song_link = 'https://www.jiosaavn.com/song/song_name/id'
    
    # create identifier
    identifier = api.create_identifier(link, 'song')

    # get trending songs
    trending_songs = api.get_trending()

    # get latest charts
    charts = api.get_charts()

    # get song link from identifier
    song_link = api.get_song_link(identifier)

    # get song details
    details = api.get_song_details(identifier)

    # get song lyrics
    lyrics = api.get_song_lyrics(identifier)

    # get download links
    download_links = api.get_download_links(identifier)

    ## Albums Service
    # get song details
    album_details = api.get_album_details(identifier)
    
    # get album songs download links
    data = api.generate_album_download_links(identifier) 
    ```

  - From Command Line

    ```bash
    python3 -m musicapy.saavn_api -h
    ```

    > Command Line Output

    ```bash
    usage: __main__.py [-h] [-t] [-c] [-d] [-l LINK] [-aD] [-a] [-sS SEARCH_SONG_QUERY] [-sA SEARCH_ALBUM_QUERY] [-sa SEARCH_ALL_QUERY]

    options:
      -h, --help            show this help message and exit
      -t, --trending        get trending songs
      -c, --charts          get charts
      -d, --download        generate download links
      -l LINK, --link LINK  link of song or album
      -aD, --album-details  get album details from link
      -a, --album           get album download links
      -sS SEARCH_SONG_QUERY, --search-song SEARCH_SONG_QUERY
                            search song by name
      -sA SEARCH_ALBUM_QUERY, --search-album SEARCH_ALBUM_QUERY
                            search album by name
      -sa SEARCH_ALL_QUERY, --search-all SEARCH_ALL_QUERY
                        search album or song by name
    ```
