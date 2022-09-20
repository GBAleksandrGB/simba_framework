from json import loads
from requests import get


def get_geo_info(environ, request):
    ip_addr = environ.get('REMOTE_ADDR', '')
    if ip_addr:
        request_url = 'https://geolocation-db.com/jsonp/'
        response = get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        request['geo'] = loads(result)


front_controllers = [
    get_geo_info,
]
