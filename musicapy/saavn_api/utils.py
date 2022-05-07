class Utils:
    @staticmethod
    def create_identifier(link: str, identifier_type: str = 'song'):
        '''Creates identifier dict used with SongService to perform various actions.

        :param link: str value containing link of the JioSaavn song/album
        :param identifier_type: str value can be of type `song` or `album`

        :return: returns dictionary with keys `type` containing identifier type i.e. `id` or `link` and `value` key containing `pids` or `token`
        :rtype: dict  
        '''
        ID = None

        identifier = {
            'type': 'id' if ID else 'link',
            'value': str(ID) if ID else Utils.extract_id_from_link(link, identifier_type)
        }

        return identifier

    @staticmethod
    def extract_id_from_link(link: str, identifier_type: str = 'album' or 'song'):
        '''Extracts id from the song or album JioSaavn URL

        :param link: str value containing song or album URL
        :param identifier_type: str value can take values `song` or `album` based on URL type

        :return: id from the URL as str
        :rtype: str
        '''
        return link.split(f'{identifier_type}/')[1].split('/')[-1]

    @staticmethod
    def generate_download_links(preview_url: str, preview_bitrate: str = '_96_p') -> dict:
        '''Generates download links from preview url extracted from previous version of Jio Saavn API

        :param preview_link: str value containing song preview URL
        :param preview_bitrate: str value containing preview bit rate, default value is `_96_p`

        :return: returns dictionary of bitrate as key and download link as urls i.e. { bitrate : download_link}
        :rtype: dict
        '''
        qualities = [
            ('_12', '12kbps'),
            ('_48', '48kbps'),
            ('_96', '96kbps'),
            ('_160', '160kbps'),
            ('_320', '320kbps')
        ]
        links = dict()
        for quality in qualities:
            id, bitrate = quality
            download_link = preview_url.replace(
                'preview.saavncdn.com', 'aac.saavncdn.com').replace(preview_bitrate, id)
            links[bitrate] = download_link

        return links

    @staticmethod
    def generate_album_song_download_links(album_details: dict) -> dict or bool:
        '''Generates album song download links from data fetched from SaavnAPI

        :param album_details: dict value containing data fetched from SaavnAPI using `AlbumService.get_album_details` static method

        :return: returns album song download links as a dictionary, if error occurs returns False
        :rtype: dict or bool
        '''
        songs_links = []
        for song in album_details.get('songs', []):
            name = song.get('perma_url', '').split('/song/')[-1].split('/')[0]
            preview_link = song.get('media_preview_url', False)
            image = song.get('image', False)
            songs_links.append(
                {"song": name, "image": image, "links": Utils.generate_download_links(preview_link)})

        return songs_links
