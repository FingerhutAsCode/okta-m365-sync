import json
import logging
import os

logger = logging.getLogger(__name__)

MAPPINGS_PATH = os.path.join(os.path.dirname(__file__), "../../config/group_mappings.json")


def _load_mappings() -> list:
    with open(MAPPINGS_PATH, "r") as f:
        return json.load(f).get("mappings", [])


def _save_mappings(mappings: list):
    with open(MAPPINGS_PATH, "r") as f:
        data = json.load(f)
    data["mappings"] = mappings
    with open(MAPPINGS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def resolve_m365_group(okta_group_id: str) -> dict | None:
    for mapping in _load_mappings():
        if mapping.get("oktaGroupId") == okta_group_id:
            return mapping
    return None


def add_group_mapping(okta_group_id: str, okta_group_name: str, m365_group_id: str):
    mappings = _load_mappings()
    mappings.append({
        "oktaGroupId": okta_group_id,
        "oktaGroupName": okta_group_name,
        "m365GroupId": m365_group_id,
        "m365GroupName": okta_group_name,
        "targetType": os.environ.get("TARGET_GROUP_TYPE", "both"),
        "autoCreate": True
    })
    _save_mappings(mappings)


def remove_group_mapping(okta_group_id: str):
    mappings = [m for m in _load_mappings() if m.get("oktaGroupId") != okta_group_id]
    _save_mappings(mappings)
