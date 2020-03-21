import requests


def get_response_about_place(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return 'Error'
    return response


def get_coordinates_place(json_responce):
    return json_responce["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["Point"]["pos"].split()

