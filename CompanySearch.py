import requests


def search_company(coordinates):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    spn = ['0.0002225', '0.0002225']  # 50 метров
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": f"{coordinates[0]},{coordinates[1]}",
        "spn": f"{spn[0]},{spn[1]}",
        "results": "1",
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        return 'Error'
    return response


def get_coompany_coords(json_responce):
    return json_responce["features"][0]["geometry"]["coordinates"]
