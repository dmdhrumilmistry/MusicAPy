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
    album_details = api.get_album_details(identifier)
    ```
