import logging
from src.shared.graph_client import GraphClient
from src.shared.mapping import resolve_m365_group

logger = logging.getLogger(__name__)

def run(event: dict):
    target = event.get("target", [{}])[0]
    actor = event.get("actor", {})
    okta_group_id = target.get("id")
    user_email = actor.get("login")
    if not okta_group_id or not user_email:
        logger.warning("Missing group or user info in event payload")
        return
    m365_group = resolve_m365_group(okta_group_id)
    if not m365_group:
        logger.info(f"No M365 mapping for Okta group {okta_group_id}")
        return
    graph = GraphClient()
    graph.add_group_member(m365_group["m365GroupId"], user_email)
    logger.info(f"Added {user_email} to M365 group {m365_group['m365GroupName']}")
