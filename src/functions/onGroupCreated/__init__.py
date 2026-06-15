import logging
import os
from src.shared.graph_client import GraphClient
from src.shared.mapping import add_group_mapping

logger = logging.getLogger(__name__)

def run(event: dict):
    if os.environ.get("AUTO_CREATE_GROUPS", "true").lower() != "true":
        return
    target = event.get("target", [{}])[0]
    okta_group_id = target.get("id")
    okta_group_name = target.get("displayName")
    if not okta_group_id or not okta_group_name:
        logger.warning("Missing group info in event payload")
        return
    graph = GraphClient()
    target_type = os.environ.get("TARGET_GROUP_TYPE", "both")
    m365_group_id = None
    if target_type in ("m365", "both"):
        m365_group_id = graph.create_m365_group(okta_group_name)
        logger.info(f"Created M365 group: {okta_group_name}")
    if target_type in ("distribution", "both"):
        graph.create_distribution_list(okta_group_name)
        logger.info(f"Created Distribution List: {okta_group_name}")
    if m365_group_id:
        add_group_mapping(okta_group_id, okta_group_name, m365_group_id)
