import time
import uuid
import random

from .auth_token_helper import get_auth_token


class RunTimeTools:
    def __init__(self):
        self.random_guid_list = []
        random.seed(time.time())

    def get_random_sleep(self, lower_range: float = 0.1, upper_range: float = 5.0) -> float:
        return random.uniform(lower_range, upper_range)

    def get_random_guid(self) -> str:
        guid = ''

        while True:
            guid = str(uuid.uuid4())

            if guid not in self.random_guid_list:
                self.random_guid_list.append(guid)
                break

        return guid

    def get_auth_token(self, client_id: str, client_secret: str, base_url: str) -> str:
        return get_auth_token(client_id=client_id, client_secret=client_secret, base_url=base_url)
