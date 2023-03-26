from json import loads as load_JSON
from requests import get as GET

from . import config
from .endpoint import get_data, get_endpoint
from .utils import Utils


import wget


class SearchService:
    ''':class:`SearchService` used to search for songs based on albums or song
    name or all. Contains implemented to search for songs and albums, returns
    data in json format as python dict.'''
    @staticmethod
    def search_song(song_query: str, page: int = 1,
                    limit: int = 20) -> dict or bool:
        '''Searchs for songs using song name and returns data based on passed
        arguments

        :param song_query: string containing name of the song
        :param page: int value used for pagination
        :param limit:  int value used for total results fetched on single page

        :return: returns a dict containing data if error occurs returns False
        :rtype: dict or bool

        '''
        return get_data('searchSong', params={'q': song_query,
                                              'page': page, 'limit': limit})

    @staticmethod
    def search_album(album_query: str, page: int = 1,
                     limit: int = 20) -> dict or bool:
        '''Search for albums

        :param album query: str containing album name
        :param page: int value containing page number
        :param limit: int value representing number of results on a single page

        :return: False if anything goes wrong else returns python dict
        containing dict
        :rtype: dict or bool
        '''
        return get_data('searchAlbum', params={'q': album_query,
                                               'page': page, 'limit': limit})

    @staticmethod
    def search_all(query: str) -> dict or bool:
        '''Search for songs and albums

        :param query: str containing query (artist, song or album name)

        :return: returns dict if no error occurs else returns False
        :rtype: dict or bool
        '''
        return get_data('searchAlbum', params={'q': query})


class SongService:
    ''':class:`SongService` class wraps various JioSaavn API functions such as
    extracting song id, encrypted url, get trending songs, charts, etc.'''
    @staticmethod
    def get_song_details(identifier: dict, use_v4=False) -> dict or bool:
        '''Get song details using identifier

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.
        :param use_v4: bool value notifying Service to use API version 4,
        default value is False

        :return: returns data in form of dict, if error occurs or data is
        absent then returns False
        :rtype: dict or bool
        '''
        # check type
        is_by_link = True if identifier.get('type', None) == 'link' else False

        # get api type
        api_type = 'songDetailsByLink' if is_by_link else 'songDetails'

        # generate params
        param = {'token' if is_by_link else 'albumid': identifier['value']}

        song_details = get_data(api_type, param, use_v4)
        
        if song_details:
            song_details = song_details.get('songs')[0]

            # extract preview urls
            preview_url = song_details.get('media_preview_url', False)

            # generate download links and return
            download_links = Utils.generate_download_links(preview_url)

            song_details['download_links'] = download_links

        return song_details

    @staticmethod
    def generate_song_download_links(identifier: dict):
        '''static method of :class:`SongService` Generates download links for
        song in various bitrate formats using identifier from JioSaavn API.

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: returns a dictionary containing song auth url, file type and
        status if error occurs then returns False
        :rtype: dict | bool
        '''
        # does not work with API version 4
        song_details = SongService.get_song_details(identifier, use_v4=False)
        
        if song_details:
            return song_details.get(
                'download_links',
                {'msg':'no media_preview_url found in song details'}
            )

        return False

    @staticmethod
    def get_song_link(identifier: dict, bitrate: str = '320') -> dict or bool:
        '''static method of :class:`SongService` Generates link for song using
        identifier from JioSaavn API.

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.
        :param  bitrate: bitrate of the song, default value 320 i.e. 320 kbps

        :return: returns a dictionary containing song auth url, file type and
        status if error occurs then returns False
        :rtype: dict | bool
        '''
        data = SongService.get_song_details(identifier)

        # extract encrypted media url
        enc_media_url = None
        if data in (None, False):
            return False
        else:
            enc_media_url = ['songs'][0]['more_info']['encrypted_media_url']

        # generate auth token
        endpoint = get_endpoint(config.api_types['songAuthToken'])
        param = {'url': enc_media_url, 'bitrate': bitrate}
        res = GET(endpoint, params=param)

        if res.status_code == 200:
            data = load_JSON(res.text.encode().decode('utf-8'))
        else:
            return False
        return data

    @staticmethod
    def get_song_id(identifier: dict) -> str or bool:
        '''Retreives Song Main Id which is used to get lyrics

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: Song Id as str if id found else False
        :rtype: str or bool
        '''
        data = SongService.get_song_details(identifier)
        return data['songs'][0].get('id', False)

    @staticmethod
    def get_trending() -> dict or bool:
        '''Get trending songs list as json data in form of dict

        :return: dict containing trending songs list
        :rtype: None or dict
        '''
        return get_data(api_type='trending')

    @staticmethod
    def get_charts() -> dict or bool:
        '''Get song charts list as json data in form of dict

        :return: dict containing charts
        :rtype: None or dict
        '''
        return get_data(api_type='charts')

    @staticmethod
    def get_song_lyrics(identifier: dict) -> str or bool:
        '''Get song lyrics

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: dict containing charts
        :rtype: dict or bool
        '''
        # get song id
        id = SongService.get_song_id(identifier)
        if not id:
            return False

        # get lyrics
        lyrics = get_data(
            'lyrics', {'lyrics_id': id}).get('lyrics', False)
        if not lyrics:
            return False

        # sanitize lyrics
        def sanitize_lyrics(data): return data.replace('<br>', '\n')
        lyrics = sanitize_lyrics(lyrics)

        return lyrics

    @staticmethod
    def save_song(identifier: dict, floc: str, bitrate: str = '320'):
        '''Saves song to local machine using identifier

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.
        :param floc: str value, containing downloaded file location
        :param  bitrate: str value, bitrate of the song, default value 320,
        i.e., 320 kbps

        :return: dict containing trending songs list
        :rtype: dict
        '''
        download_url = SongService.get_song_link(identifier, bitrate)
        result = wget.download(download_url['auth_url'], out=floc, bar=False)
        return result


class AlbumService:
    ''':class:`AlbumService` class provides JioSaavn API wrapper class to
    perform operations on albums'''

    @staticmethod
    def get_album_details(identifier: dict) -> dict or bool:
        '''Fetches album details and returns it as dict

        :param identifier: dict, containing identifier type and its value.

        :return: returns album details as dict, if error occurs returns False
        :rtype: dict or bool
        '''
        id_type = identifier.get('type')
        id_value = identifier.get('value')

        if id_type == 'link':
            api_type = 'albumDetailsByLink'
            param = {'token': id_value}
        elif id_type == 'id':
            api_type = 'albumDetails'
            param = {'albumid': id_value}

        album_details = get_data(api_type, param, use_v4=False)

        if album_details:
            songs_details = []
            for song in album_details.get('songs',[]):
                perma_url = song.get('perma_url')
                song_identifier = Utils.create_identifier(perma_url, 'song')
                song_details = SongService.get_song_details(song_identifier, use_v4=False)
                songs_details.append(song_details)
                
            album_details['songs'] = songs_details

        # make get request and return data
        return album_details

    @staticmethod
    def generate_album_download_links(identfier: dict) -> dict or bool:
        '''Generates album song download links and returns it as dict

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: returns details along with song download links as dict, if
        error occurs returns False
        :rtype: dict or bool
        '''
        album_details = AlbumService.get_album_details(identfier)

        data = {
            "album_id": album_details.get('albumid', False),
            "album_title": album_details.get('title', False),
            "album_year": album_details.get('title', False),
            "album_image": album_details.get('image', False),
            "perma_url": album_details.get('perma_url', False),
            "primary_artist": album_details.get('primary_artists', False),
            "primary_artist_id": album_details.get('primary_artists_id',
                                                   False),
            "songs": Utils.generate_album_song_download_links(album_details)
        }

        return data


class PlaylistService:
    ''':class:`PlaylistService` class provides JioSaavn API wrapper class to
    perform operations on playlists'''

    @staticmethod
    def get_playlist_details(identifier):
        '''Fetches Playlist details returns it as dict

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: returns playlist details along with songs download links
        :rtype: dict
        '''
        id_type = identifier.get('type')
        id_value = identifier.get('value')

        playlist_details = None
        if id_type == 'link':
            api_type = 'playlistDetailsByLink'
            param = {
                'token': id_value,
                'n':9999 # number of songs ## temporary fix instead of using pagination
                # 'p' : 1 ## TODO: for pagination
            }
            use_v4 = False
            
        elif id_type == 'id':
            api_type = 'playlistDetails'
            param = {'listid': id_value}
            use_v4 = True

        playlist_details = get_data(api_type, param, use_v4)

        if not playlist_details:
            return None
        
        # add download links to songs
        if id_type == 'link':
            song_details = PlaylistService.__get_playlist_song_download_links_by_link(playlist_details)
        elif id_type == 'id':
            song_details = PlaylistService.__get_playlist_song_download_links_by_id(playlist_details)

        playlist_details['songs'] = song_details

        return playlist_details


    @staticmethod
    def get_playlist_song_download_links(identifier):
        '''Fetches Songs details from a playlist with download links and 
        returns it as dict

        :param identifier: dictionary containing `type` and `value` as keys
        containing type(id or link) and its value(pids or token) respectively
        for JioSaavn API.

        :return: returns playlist songs details and download links as dict, if
        error occurs returns False
        :rtype: dict or bool
        '''
        res = PlaylistService.get_playlist_details(identifier)

        if not res:
            return None
        
        return res.get('songs', None)
    
    @staticmethod
    def __get_playlist_song_download_links_by_link(playlist_details:dict) -> dict:
        '''Generates song download links using playlist details fetched from API
        using link and returns it as dict.

        :param playlist_details: dictionary containing playlist details fetched
        from jiosaavn API.

        :return: returns playlist songs details and download links as dict.
        :rtype: dict or bool
        '''
        song_details = playlist_details.get('songs', {})
        for song in song_details:
            preview_link = song.get('media_preview_url', False)
            download_links = Utils.generate_download_links(preview_link) if preview_link else None
            song['download_links'] = download_links

        return song_details
    
    @staticmethod
    def __get_playlist_song_download_links_by_id(playlist_details:dict) -> list:
        '''Generates song download links using playlist details fetched from API
        using listid and returns it as dict.

        :param playlist_details: dictionary containing playlist details fetched
        from jiosaavn API.

        :return: returns playlist songs details and download links as dict.
        :rtype: dict or bool
        '''
        songs_list = playlist_details.get('list', [])
        songs_details = []

        # TODO: fetch songs asynchronously
        for song in songs_list:
            perma_url = song.get('perma_url')
            song_identifier = Utils.create_identifier(perma_url, 'song')
            song_details = SongService.get_song_details(song_identifier, use_v4=False)
            songs_details.append(song_details)

        return songs_details
