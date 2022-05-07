headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/plain, */*',
    'Cache-Control': 'no-cache',
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.jiosaavn.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
}

base_url = 'https://www.jiosaavn.com/api.php?_format=json&_marker=0&ctx=web6dot0'

api_types = {
    #  search
    'searchAll': 'autocomplete.get',
    'searchSong': 'search.getResults',          # supports pagination
    'searchAlbum': 'search.getAlbumResults',    # supports pagination
    'searchArtist': 'search.getArtistResults',  # supports pagination

    # details by id
    'songDetails': 'song.getDetails',
    'albumDetails': 'content.getAlbumDetails',

    # details by link
    'songDetailsByLink': 'webapi.get&type=song',
    'albumDetailsByLink': 'webapi.get&type=album',

    # misc
    'homeData': 'webapi.getLaunchData',
    'charts': 'content.getCharts',
    'trending': 'content.getTrending',
    'albums': 'content.getAlbums',              # supports pagination
    'lyrics': 'lyrics.getLyrics',

    # generate auth token
    'songAuthToken': 'song.generateAuthToken'   # need encrypted url which can be received from song details `encrypted_media_url` field
}
