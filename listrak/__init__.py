import requests
import os
from datetime import datetime, timedelta

from . import api

class Listrak:
    """https://api.listrak.com/email
    """
    def __init__(self, client_id, client_secret):
        self.root_endpoint = "https://api.listrak.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_data = self.get_auth_token_data()

        self.email = api.Email(self.root_endpoint, self.bearer_token)

    def get_auth_token_data(self) -> None:
        """Authenticate using OAuth 2.0.
        Returns bearer token which is used for all subsequent API calls.
        Datetime is calculated for when the bearer token will expire (1 hour).
        https://api.listrak.com/email#section/Authentication
        """
        body = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        r = requests.post("https://auth.listrak.com/OAuth2/Token", data=body)
        try:
            r.raise_for_status()
            auth_token_data = r.json()
            self.bearer_token = auth_token_data["access_token"]
            self.bearer_token_expire_dt = datetime.now() + timedelta(seconds=auth_token_data["expires_in"])
        except requests.exceptions.HTTPError as e:
            print(e)
        return

    def refresh_bearer_token_if_expired(self) -> bool:
        """Check if bearer token expiration date has passed.
        If the bearer token is expired, a new one will be retrieved to replace it.

        Returns:
            bool: Returns True if the bearer token was expired. False means no update was necessary.
        """
        if self.bearer_token_expire_dt < datetime.now():
            get_auth_token_data(self)
            return True
        else:
            return False
