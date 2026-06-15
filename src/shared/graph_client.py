import logging
import os
import requests
from msal import ConfidentialClientApplication

logger = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/.default"]


class GraphClient:
    def __init__(self):
        self._token = self._acquire_token()

    def _acquire_token(self) -> str:
        app = ConfidentialClientApplication(
            client_id=os.environ["AZURE_CLIENT_ID"],
            client_credential=os.environ["AZURE_CLIENT_SECRET"],
            authority=f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}"
        )
        result = app.acquire_token_for_client(scopes=SCOPES)
        if "access_token" not in result:
            raise RuntimeError(f"Failed to acquire Graph token: {result.get('error_description')}")
        return result["access_token"]

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}

    def add_group_member(self, group_id: str, user_email: str):
        user = self._get_user_id(user_email)
        url = f"{GRAPH_BASE}/groups/{group_id}/members/$ref"
        payload = {"@odata.id": f"{GRAPH_BASE}/directoryObjects/{user}"}
        r = requests.post(url, json=payload, headers=self._headers())
        r.raise_for_status()

    def remove_group_member(self, group_id: str, user_email: str):
        user_id = self._get_user_id(user_email)
        url = f"{GRAPH_BASE}/groups/{group_id}/members/{user_id}/$ref"
        r = requests.delete(url, headers=self._headers())
        r.raise_for_status()

    def create_m365_group(self, display_name: str) -> str:
        payload = {
            "displayName": display_name,
            "mailEnabled": True,
            "mailNickname": display_name.replace(" ", "-").lower(),
            "securityEnabled": False,
            "groupTypes": ["Unified"]
        }
        r = requests.post(f"{GRAPH_BASE}/groups", json=payload, headers=self._headers())
        r.raise_for_status()
        return r.json()["id"]

    def create_distribution_list(self, display_name: str) -> str:
        payload = {
            "displayName": display_name,
            "mailEnabled": True,
            "mailNickname": display_name.replace(" ", "-").lower(),
            "securityEnabled": False
        }
        r = requests.post(f"{GRAPH_BASE}/groups", json=payload, headers=self._headers())
        r.raise_for_status()
        return r.json()["id"]

    def delete_group(self, group_id: str):
        r = requests.delete(f"{GRAPH_BASE}/groups/{group_id}", headers=self._headers())
        r.raise_for_status()

    def _get_user_id(self, email: str) -> str:
        r = requests.get(f"{GRAPH_BASE}/users/{email}", headers=self._headers())
        r.raise_for_status()
        return r.json()["id"]
