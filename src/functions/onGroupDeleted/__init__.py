import logging
from src.shared.graph_client import GraphClient
from src.shared.mapping import resolve_m365_group, remove_group_mapping

logger = logging.getLogger(__name__)

def run(event: dict):
    target = event.get("target", [{}])[0]
    okta_group_id = target.get("id")
    if not okta_group_id:
        logger.warning("Missing group ID in event payload")
        return
    m365_group = resolve_m365_group(okta_group_id)
    if not m365_group:
        logger.info(f"No M365 mapping for Okta group {okta_group_id}")
        return
    graph = GraphClient()
    graph.delete_group(m365_group["m365GroupId"])
    remove_group_mapping(okta_group_id)
    logger.info(f"Deleted M365 group {m365_group['m365GroupName']}")
