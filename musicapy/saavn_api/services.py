from . import config
from .utils import Utils
from .endpoint import get_endpoint, get_data
from requests import get as GET
from json import loads as load_JSON
import wget


class SearchService:
    ''':class:`SearchService` used to search for songs based on albums or song name or all. Contains implemented to search for songs and albums, returns data in json format as python dict.
    '''
    @staticmethod
    def search_song(song_query: str, page: int = 1, limit: int = 20) -> dict or bool:
        '''Searchs for songs using song name and returns data based on passed arguments

        :param song_query: string containing name of the song
        :param page: int value used for pagination
        :param limit:  int value used for total results fetched on single page

        :return: returns a dict containing data if error occurs returns False
        :rtype: dict or bool

        '''
        return get_data('searchSong', params={'q': song_query, 'page': page, 'limit': limit})

    @staticmethod
    def search_album(album_query: str, page: int = 1, limit: int = 20) -> dict or bool:
        '''Search for albums

        :param album query: str containing album name
        :param page: int value containing page number
        :param limit: int value representing number of results on a single page

        :return: False if anything goes wrong else returns python dict containing dict  
        :rtype: dict or bool
        '''
        return get_data('searchAlbum', params={'q': album_query, 'page': page, 'limit': limit})

    @staticmethod
    def search_all(query: str) -> dict or bool:
        '''Search for songs and albums

        :param query: str containing query (artist, song or album name)

        :return: returns dict if no error occurs else returns False
        :rtype: dict or bool
        '''
        return get_data('searchAlbum', params={'q': query})


class SongService:
    ''':class:`SongService` class wraps various JioSaavn API functions such as extracting song id, encrypted url, get trending songs, charts, etc.'''
    @staticmethod
    def get_song_details(identifier: dict, use_v4=False) -> dict or bool:
        '''Get song details using identifier

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.
        :param use_v4: bool value notifying Service to use API version 4, default value is False

        :return: returns data in form of dict, if error occurs or data is absent then returns False
        :rtype: dict or bool
        '''
        # check type
        is_by_link = True if identifier.get('type', None) == 'link' else False

        # get api type
        api_type = 'songDetailsByLink' if is_by_link else 'songDetails'

        # generate params
        param = {'token' if is_by_link else 'pids': identifier['value']}

        data = get_data(api_type, param, use_v4)
        return data

    @staticmethod
    def get_download_links(identifier: dict):
        '''static method of :class:`SongService` Generates download links for song in various bitrate formats using identifier from JioSaavn API.

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.

        :return: returns a dictionary containing song auth url, file type and status if error occurs then returns False
        :rtype: dict | bool
        '''
        # does not work with API version 4
        song_details = SongService.get_song_details(identifier, use_v4=False)
        if song_details == False:
            return False

        # extract preview urls
        preview_url = song_details['songs'][0].get('media_preview_url', False)
        if not preview_url:
            return False

        # generate download links and return
        download_links = Utils.generate_download_links(preview_url)
        return download_links

    @staticmethod
    def get_song_link(identifier: dict, bitrate: str = '320') -> dict or bool:
        '''static method of :class:`SongService` Generates link for song using identifier from JioSaavn API.

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.
        :param  bitrate: bitrate of the song, default value 320 i.e. 320 kbps

        :return: returns a dictionary containing song auth url, file type and status if error occurs then returns False
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

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.

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

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.

        :return: dict containing charts
        :rtype: dict or bool
        '''
        # get song id
        id = SongService.get_song_id(identifier)
        if id == False:
            return False

        # get lyrics
        lyrics = get_data(
            'lyrics', {'lyrics_id': id}).get('lyrics', False)
        if lyrics == False:
            return False

        # sanitize lyrics
        def sanitize_lyrics(data): return data.replace('<br>', '\n')
        lyrics = sanitize_lyrics(lyrics)

        return lyrics

    @staticmethod
    def save_song(identifier: dict, floc: str, bitrate: str = '320'):
        '''Saves song to local machine using identifier

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.
        :param floc: str value, containing downloaded file location
        :param  bitrate: str value, bitrate of the song, default value 320 i.e. 320 kbps

        :return: dict containing trending songs list
        :rtype: dict
        '''
        download_url = SongService.get_song_link(identifier, bitrate)
        result = wget.download(download_url['auth_url'], out=floc, bar=False)
        return result


class AlbumService:
    ''':class:`AlbumService` class provides JioSaavn API wrapper class to perform operations on albums'''

    @staticmethod
    def get_album_details(identifier: dict) -> dict or bool:
        '''Fetches album details and returns it as dict

        :param album_query: str value, can be album link or album name

        :return: returns album details as dict, if error occurs returns False
        :rtype: dict or bool
        '''
        # check type
        is_by_link = True if identifier.get('type', False) == 'link' else False

        # get api type
        api_type = 'albumDetailsByLink' if is_by_link else 'albumDetails'

        # generate params
        param = {'token' if is_by_link else 'pids': identifier['value']}

        # make get request and return data
        data = get_data(api_type, param, use_v4=False)
        return data

    @staticmethod
    def generate_album_download_links(identfier: dict) -> dict or bool:
        '''Generates album song download links and returns it as dict

        :param identifier: dictionary containing `type` and `value` as keys containing type(id or link) and its value(pids or token) respectively for JioSaavn API.

        :return: returns details along with song download links as dict, if error occurs returns False
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
            "primary_artist_id": album_details.get('primary_artists_id', False),
            "songs": Utils.generate_album_song_download_links(album_details)
        }

        return data
