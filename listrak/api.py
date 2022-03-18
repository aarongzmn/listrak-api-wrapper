import requests


class Email:
    """Listrak API Email endpoint
    https://api.listrak.com/email

    Args:
        bearer_token (str): Auth token used for the Listrak API
    """
    def __init__(self, host, bearer_token):
        self.host = host
        self.bearer_token = bearer_token

    def get_a_list(self, list_id) -> dict:
        """Returns the specified list.
        https://api.listrak.com/email#operation/List_GetListResourceById
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self.host + f"/email/v1/List/{list_id}", headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("data")
        except requests.exceptions.HTTPError as e:
            print(e)

    def get_all_lists(self) -> list:
        """Returns your account's collection of lists.
        https://api.listrak.com/email#operation/List_GetListCollection
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self.host + "/email/v1/List", headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("data")
        except requests.exceptions.HTTPError as e:
            print(e)
