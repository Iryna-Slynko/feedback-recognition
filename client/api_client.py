import requests
from requests.structures import CaseInsensitiveDict


class ApiClient:
    def __init__(self, address, client_id, client_token):
        self.__address__ = address
        self.__client_id__ = client_id
        self.__client_token__ = client_token

    def record(self, result):
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        requests.post(
            self.address,
            params={
                client: self.__client_id__,
                token: self.__client_token__,
                upvote: result,
            },
            headers=headers,
        )
