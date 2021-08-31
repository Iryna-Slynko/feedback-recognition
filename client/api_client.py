import requests
from requests.structures import CaseInsensitiveDict
import json


class ApiClient:
    def __init__(self, address, client_id, client_token):
        self.__address__ = address
        self.__client_id__ = client_id
        self.__client_token__ = client_token

    def record(self, result):

        resp = requests.post(
            self.__address__,
            data=json.dumps(
                {
                    "client": self.__client_id__,
                    "token": self.__client_token__,
                    "upvote": result,
                }
            ),
            headers={"Content-Type": "application/json"},
        )
