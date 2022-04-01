import requests
from datetime import datetime, timedelta

from . import email


class Listrak:
    """https://api.listrak.com/email
    """
    def __init__(self, client_id, client_secret):
        self._root_endpoint = "https://api.listrak.com"
        self._client_id = client_id
        self._client_secret = client_secret

        self._get_auth_token_data()

        self.uri_list = email.ListEndpoint(self._root_endpoint, self._bearer_token)
        self.uri_list_import = email.ListImportEndpoint(self._root_endpoint, self._bearer_token)
        self.uri_contact = email.ContactEndpoint(self._root_endpoint, self._bearer_token)
        self.uri_segmentation_field = email.SegmentationFieldEndpoint(self._root_endpoint, self._bearer_token)
        self.uri_segmentation_field_group = email.SegmentationFieldGroupEndpoint(self._root_endpoint, self._bearer_token)

    def get_auth_token_data(self) -> None:
        """Authenticate using OAuth 2.0.
        Helper function used to check if bearer token has expired.
        If the bearer token has expired, it will be replaced by a new one.
        """
        if datetime.now() >= self._auth_expire_dt:
            print("Listrak API token expired, getting new token.")
            self._get_auth_token_data()
            return
        else:
            return

    def _get_auth_token_data(self) -> None:
        """Authenticate using OAuth 2.0.
        Returns bearer token which is used for all subsequent API calls.
        Datetime is calculated for when the bearer token will expire (1 hour).
        https://api.listrak.com/email#section/Authentication
        """
        body = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }
        r = requests.post("https://auth.listrak.com/OAuth2/Token", data=body)
        try:
            r.raise_for_status()
            auth_token_data = r.json()
            self._bearer_token = auth_token_data["access_token"]
            expires_in = auth_token_data["expires_in"]
            self._auth_expire_dt = datetime.now() + timedelta(seconds=expires_in)
        except requests.exceptions.HTTPError as e:
            print(e)
        return
