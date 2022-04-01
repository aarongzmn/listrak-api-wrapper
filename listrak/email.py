import requests
from datetime import datetime
from typing import Literal


class ListEndpoint:
    """Lists represent groupings of contacts, messages, and more.
    Listrak's Email API is list-centric, just like Listrak's application.
    Most resources available through this API are associated with a specific list.
    https://api.listrak.com/email#tag/List
    """
    def __init__(self, root_endpoint, bearer_token):
        self.endpoint = root_endpoint + "/email/v1/List"
        self.bearer_token = bearer_token

    def get_all_lists(self) -> dict:
        """Returns your account's collection of lists.
        https://api.listrak.com/email#operation/List_GetListCollection
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self.endpoint, headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("data")
        except requests.exceptions.HTTPError as e:
            print(e)

    def create_a_list_(
        self,
        list_name: str,
        bounce_handling: Literal["None", "Standard", "Aggressive"] = "None",
        bounce_unsubscribe_count: int = 1
        ) -> dict:
        """Creates a new list in your account.
        https://api.listrak.com/email#operation/List_PostListResource

        Args:
            list_name (str): Name of the list.
            bounce_handling (str, optional): Bounce handling method for the list.
                Allowed values are 'None', 'Standard', and 'Aggressive'.
            bounce_unsubscribe_count (int, optional): The number of bounces that are allowed before being automatically unsubscribed.

        Returns:
            dict: If success dict will contain 'status':int and 'resourceId':str keys.
                If fail dict will 'status':int code, 'error':string, and 'message':string keys.
        """
        data = {
            "list_name": list_name,
            "bounceHandling": bounce_handling,
            "bounceUnsubscribeCount": bounce_unsubscribe_count,
        }
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.post(self.endpoint, data=body, headers=headers)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(e)

    def get_a_list(self, list_id: int) -> dict:
        """Returns the specified list.
        https://api.listrak.com/email#operation/List_GetListResourceById
        Args:
            list_id (int): Identifier used to locate the list.

        Returns:
            dict: If success dict will contain 'status':int and 'data':dict keys.
                If fail dict will 'status':int code, 'error':string, and 'message':string keys.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self.endpoint + f"/{list_id}", headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("data")
        except requests.exceptions.HTTPError as e:
            print(e)

    def update_a_list_(
        self,
        list_id,
        list_name: str,
        bounce_handling: Literal["None", "Standard", "Aggressive"] = "None",
        bounce_unsubscribe_count: int = 1,
        ) -> dict:
        """Returns your account's collection of lists.
        https://api.listrak.com/email#operation/List_PutListResource
        Args:
            list_name (str): Name of the list.
            bounce_handling (str, optional): Bounce handling method for the list.
                Allowed values are 'None', 'Standard', and 'Aggressive'.
            bounce_unsubscribe_count (int, optional): The number of bounces that are allowed before being automatically unsubscribed.

        Returns:
            dict: If success dict will contain 'status':int and 'resourceId':str keys.
                If fail dict will 'status':int code, 'error':string, and 'message':string keys.
        """
        data = {
            "list_name": list_name,
            "bounceHandling": bounce_handling,
            "bounceUnsubscribeCount": bounce_unsubscribe_count,
        }
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.put(self.endpoint + f"/{list_id}", data=body, headers=headers)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(e)

    def delete_a_list(self, list_id: int) -> dict:
        """Deletes the specified list.
        https://api.listrak.com/email#operation/List_DeleteListResource

        Args:
            list_id (int): Identifier used to locate the list.

        Returns:
            dict: If success dict will contain 'status':int key.
                If fail dict will 'status':int code, 'error':string, and 'message':string keys.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.delete(self.endpoint + f"/{list_id}", headers=headers)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(e)


class ListImportEndpoint:
    """The List Import resource is used to supply an import file in order to import data to a list.
    https://api.listrak.com/email#tag/ListImport
    """
    def __init__(self, root_endpoint, bearer_token):
        self.endpoint = root_endpoint + "/email/v1/List"
        self.bearer_token = bearer_token

    def get_all_list_imports(self, list_id) -> dict:
        """Retrieves the collection of list imports associated with the specified list.
        https://api.listrak.com/email#operation/ListImport_GetListImportCollection
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.get(self.endpoint + f"/{list_id}/ListImport", headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("data")
        except requests.exceptions.HTTPError as e:
            print(e)

    def start_a_list_import(
        self,
        list_id: int,
        file_stream: str,
        file_mappings_segmentation_field_id: int,
        file_mappings_default_value: str,
        file_mappings_file_column: int = 0,
        file_mappings_file_column_type: Literal["Email", "SegmentationField", "Event"] = "Email",
        file_delimiter: str = ",",
        file_name: str = str(datetime.now())[0:16].replace(" ", "@").replace(":", ""),
        has_column_names: bool = True,
        import_type: Literal["AddSubscribers", "AddSubscribersAndSegmentationData", "RemoveSubscribers", "UpdateSubscribers"] = "AddSubscribers",
        segentation_import_type: Literal["Update", "Append", "Overwrite"] = "",
        suppress_email_notifications: bool = False,
        text_qualifier: str = '"'
        ) -> str:
        """Creates and starts a new import for the specified list.
        https://api.listrak.com/email#operation/ListImport_GetListImportCollection

        Returns the 'resourceId': An identifier used to locate a resource.
        """
        body = {
            "fileDelimiter": file_delimiter,
            "fileMappings": {
                "segmentationFieldId": file_mappings_segmentation_field_id,
                "defaultValue": file_mappings_default_value,
                "fileColumn": file_mappings_file_column,
                "fileColumnType": file_mappings_file_column_type
            },
            "fileName": file_name,
            "fileStream": file_stream,
            "hasColumnNames": has_column_names,
            "importType": import_type,
            "segmentationImportType": segentation_import_type,
            "suppressEmailNotifications": suppress_email_notifications,
            "textQualifier": text_qualifier
        }

        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r = requests.post(self.endpoint + f"/{list_id}/ListImport", data=body, headers=headers)
        try:
            r.raise_for_status()
            return r.json().get("resourceId")
        except requests.exceptions.HTTPError as e:
            print(e)


class ContactEndpoint:
    """The Contact resource is used to add, update and remove new contacts to a List. This resource also exposes the ability to set a contact's profile fields and subscription state.
    https://api.listrak.com/email#tag/Contact
    """
    def __init__(self, root_endpoint, bearer_token):
        self.endpoint = root_endpoint + "/email/v1/List"
        self.bearer_token = bearer_token

    def get_all_contacts(self, list_id: int) -> list:
        """Returns the collection of contacts associated with the specified list.
        https://api.listrak.com/email#operation/Contact_GetContactCollection

        TODO: Add parameter query filters, see Listrak documentation
        """
        all_contacts = []

        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        endpoint = self.endpoint + f"/{list_id}/Contact"
        r = requests.get(endpoint, headers=headers)
        all_contacts.extend(r.json()["data"])
        next_page_cursor = r.json()["nextPageCursor"]

        while next_page_cursor is not None:
            r = requests.get(endpoint + f"?cursor={next_page_cursor}", headers=headers)
            try:
                r.raise_for_status()
                all_contacts.extend(r.json()["data"])
                next_page_cursor = r.json()["nextPageCursor"]
            except requests.exceptions.HTTPError as e:
                print(e)

        return all_contacts

    def create_or_update_a_contact(
        self,
        list_id: int,
        email_address: str,
        segmentation_field_values: [{"segmentationFieldId": int,"value": str}],
        subscription_state: Literal["Subscribed", "Unsubscribed"] = "Subscribed",
        external_contact_id: str = None,
        event_ids: str = None,
        new_email_address: str = None,
        override_unsubscribe: bool = False,
        subscribed_by_contact: bool = False,
        send_double_opt_in: bool = False,
        update_type: Literal["Update", "Append", "Overwrite"] = "Update",
        ) -> str:
        """Creates or updates a contact on the specified list.
        https://api.listrak.com/email#operation/Contact_PostContactResource

        Args:
            email_address (str): Email address of the contact
            segmentation_field_values (list): Profile field values associated with the contact.
            subscription_state (Literal['Subscribed', 'Unsubscribed']): Subscription state of the contact. Defaults to 'Subscribed'.
            external_contact_id (str, optional): External contact ID provided by the client. Defaults to None.
            event_ids (str, optional): Comma-separated list of event identifiers that should be raised after the contact is created or updated. Defaults to None.
            new_email_address (str, optional): If updating an existing contact, the contact's email address will be changed to this value. Provide the original email address in the emailAddress body field to select the existing contact. Defaults to None.
            override_unsubscribe (bool, optional): Whether a contact in an unsubscribed state should be forced to a subscribed state. Defaults to False.
            subscribed_by_contact (bool, optional): Whether the subscribe was initiated by the contact. Defaults to False.
            send_double_opt_in (bool, optional): Whether a double opt-in email should be sent if a new contact is being created. Defaults to False.
            update_type (Literal['Update', 'Append', 'Overwrite'], optional): If updating an existing contact, the type of update that will be performed on any submitted profile fields. Defaults to "Update".

        Returns:
            str: 'resourceId' which is an identifier used to locate the updated resource.
        """
        body = {
            "emailAddress": email_address,
            "segmentationFieldValues": segmentation_field_values
        }
        if external_contact_id:
            body["externalContactID"] = external_contact_id
        if subscription_state:
            body["subscriptionState"] = subscription_state
        print(body)
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        endpoint = self.endpoint + f"/{list_id}/Contact"
        r = requests.post(endpoint, json=body, headers=headers)
        try:
            r.raise_for_status()
            return r.json()["resourceId"]
        except requests.exceptions.HTTPError as e:
            print(e)

    def get_a_contact(
        self,
        list_id: int,
        contact_identifier: str,
        segmentation_field_values: list = None
        ) -> dict:
        """Returns a contact by email address or by Listrak email key.
        https://api.listrak.com/email#operation/Contact_GetContactResourceByIdentifier

        Args:
            list_id (int): Identifier used to locate the list.
            contact_identifier (str): Identifier used to locate the contact. You may specify either an email address or a Listrak email key.
            segmentation_field_values (list): Comma-separated list of profile field IDs to retrieve. Up to 30 fields may be included.

        Returns:
            dict: Attributes related to contact tied to 'contact_identifier'
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        endpoint = self.endpoint + f"/{list_id}/Contact/{contact_identifier}"
        r = requests.get(endpoint, headers=headers)
        try:
            r.raise_for_status()
            return r.json()["data"]
        except requests.exceptions.HTTPError as e:
            print(e)



class SegmentationFieldEndpoint:
    """A Profile Field is used to store data about a contact so that it can be filtered in the future.
    https://api.listrak.com/email#tag/SegmentationField
    """
    def __init__(self, root_endpoint, bearer_token):
        self.endpoint = root_endpoint + "/email/v1/List"
        self.bearer_token = bearer_token

    def get_all_profile_fields(
        self,
        list_id: int,
        segmentation_field_group_id: int
        ) -> list:
        """Returns the collection of profile fields that exist for the specified profile field group.
        https://api.listrak.com/email#operation/SegmentationField_GetSegmentationFieldCollection

        Args:
            list_id (int): Identifier used to locate the list.
            segmentation_field_group_id (str): Identifier used to locate the profile field group.

        Returns:
            dict: Returns the collection of profile fields that exist for the specified profile field group.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        endpoint = self.endpoint + f"/{list_id}/SegmentationFieldGroup/{segmentation_field_group_id}/SegmentationField"
        r = requests.get(endpoint, headers=headers)
        try:
            r.raise_for_status()
            return r.json()["data"]
        except requests.exceptions.HTTPError as e:
            print(e)


class SegmentationFieldGroupEndpoint:
    """A Profile Field Group is used to group the profile fields for a given list.
    https://api.listrak.com/email#tag/SegmentationFieldGroup
    """
    def __init__(self, root_endpoint, bearer_token):
        self.endpoint = root_endpoint + "/email/v1/List"
        self.bearer_token = bearer_token

    def get_all_profile_field_groups(self, list_id: int) -> list:
        """Returns the collection of profile fields that exist for the specified profile field group.
        https://api.listrak.com/email#operation/SegmentationField_GetSegmentationFieldCollection

        Args:
            list_id (int): Identifier used to locate the list.

        Returns:
            dict: Returns a collection of profile field groups for the specified list.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        endpoint = self.endpoint + f"/{list_id}/SegmentationFieldGroup"
        r = requests.get(endpoint, headers=headers)
        try:
            r.raise_for_status()
            return r.json()["data"]
        except requests.exceptions.HTTPError as e:
            print(e)

