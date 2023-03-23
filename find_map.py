#!/usr/bin/env python

__doc__ = """
Yêu cầu:
Viết script tìm 50 quán bia / quán nhậu / quán bar /
nhà hàng quanh toạ độ của lớp học (lên google map để lấy) với bán kính 2KM.
Ghi kết quả theo định dạng JSON vào file pymi_beer.geojson

Sử dụng Google Map API
https://developers.google.com/places/web-service/

Chú ý: phải tạo "token" để có thể truy cập API -
phải tạo tài khoản google cloud,
cần có thẻ thanh toán online quốc tế (VISA/Mastercard).
Học viên không có thẻ thì đi làm thẻ.

Chú ý: giữa mỗi trang kết quả phải đợi để lấy tiếp.

Chú ý: tránh đặt ngược lat/long

- Kết quả trả về lưu theo format JSON,
với mỗi điểm là một GeoJSON point (https://leafletjs.com/examples/geojson/),
up file này lên GitHub để xem bản đồ kết quả.
"""

import requests
import json
import sys
import log
from bs4 import BeautifulSoup

logger = log.get_logger(__name__)


def get_geo_map(type_place: int) -> dict:
    """
    Get geopoint of place type :keyword: by Google API

    Input: bar
    Output: result = {Geo Point}

    :param keyword: str
    :rtype dict:
    """

    result = {}

    lat = 21.0125204
    lng = 105.8215205

    # My teacher said that I should not up my token in this code
    api_token = "_"

    map_url = "https://maps.googleapis.com/maps"
    nearby_url = f"{map_url}/place/nearbysearch"
    place = f"type={type_place}&keyword=pub&key={api_token}"
    request = f"location={lat}%2C{lng}&radius=2000&{place}"
    url = f"{nearby_url}/json?{request}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        d["geometry"]["location"]["lng"],
                        d["geometry"]["location"]["lat"],
                    ],
                },
                "properties": {"address": d["vicinity"], "name": d["name"]},
            }
            for d in data["results"]
        ],
    }

    result = geojson
    return geojson


def solve(type_place):
    """Function `solve` dùng để `test`

    :param keyword: number
    :rtype list:
    """

    logger.debug(f"""Get point in maps of type place:
        {type_place} by Google API""")
    result = get_geo_map(type_place)
    return result


def main():
    type_place = sys.argv[1]
    with open("new_map.geojson", "w") as f:
        json.dump(solve(type_place), f)


if __name__ == "__main__":
    main()
