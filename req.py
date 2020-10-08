import unittest
from typing import Dict

import requests
from requests import Response

"""
1. Attributes and Methods of requests.Response
https://www.w3schools.com/python/ref_requests_response.asp

2. HTTP Response Codes
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""


def http_get(url: str, params: Dict[str, str] = dict(), username: str = "", password: str = "", ) -> Response:
    """
    Sends a HTTP GET request to the URL with optional authentication and parameters
    :param url: URL to send the request to
    :param username: For authentication
    :param password: For authentication
    :param params: Parameters attached to URL (https://stripe.com/jobs/search?l=singapore&q=intern)
    :return: The HTTP response
    """
    if username and password:
        return requests.get(url, auth=(username, password), params=params)
    print(f"GET : {url}")
    return requests.get(url, params=params)


def http_post(url: str):
    """
    Sends a HTTP POST request to the URL with optional authentication and parameters
    :param url: URL to send the request to
    :return: The HTTP response
    """
    print(f"POST : {url}")
    return requests.post(url)


def save_image(res: Response, name: str, dest: str = "./images/"):
    if not res.ok:
        raise ValueError(f"Invalid response with status code {res.status_code}")
    if not name.endswith((".jpg", ".jpeg", ".png")):
        name += ".png"
    f = open(f"{dest}{name}", "wb")
    f.write(res.content)
    f.close()


class TestRequestMethods(unittest.TestCase):
    def test_http_get(self):
        url = "http://httpbin.org/get"
        res = http_get(url)
        self.assertEqual(url, res.url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(True, res.ok)

    def test_http_post(self):
        url = "http://httpbin.org/post"
        res = http_post(url)
        self.assertEqual(url, res.url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(True, res.ok)

    def test_save_image(self):
        pass


if __name__ == "__main__":
    unittest.main()
