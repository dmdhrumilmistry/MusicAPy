from . import config
from requests import get as GET
from json import loads as load_JSON


def get_endpoint(api: str, is_version_4: bool = True) -> str:
    '''Get endpoint url

    :param api: str value, api call from apis.saavnAPI.config module
    :param is_version_4: bool value, if True uses API version 4, else ignores it

    :return: str value containing JioSaavn API endpoint
    :rtype: str
    '''
    return f'{config.base_url}{"&api_version=4" if is_version_4 else ""}&__call={api}'


def get_data(api_type: str = '', params: dict = None, use_v4: bool = True) -> dict or bool:
    '''Sends HTTP GET request to the Saavn API server and returns data in python dict format 

    :param api_type: str value containing Saavn api method from apis.saavnAPI.config module
    :param params: dict value containing query key-value pairs
    :param use_v4: bool value. If True uses API v4 else ignores it. default value `True`

    :return: returns a dict containing data else returns False if any status code is not 200
    :rtype: dict or bool
    '''
    endpoint = get_endpoint(config.api_types[api_type], use_v4)
    res = GET(endpoint, params=params)
    data = False
    if res.status_code == 200:
        data = load_JSON(res.text)

    return data
