import requests


def get_auth_token(client_id: str, client_secret: str, base_url: str) -> str:

    auth_token_request = \
        requests.post(base_url + "/user/login", verify=False,
                      headers={
                          "Content-Type": "application/json; charset=utf-8"
                      },
                      json={
                          "email": client_id,
                          "password": client_secret
                      }
                      )

    json_repsonse = auth_token_request.json()
    
    return json_repsonse['auth_token']
