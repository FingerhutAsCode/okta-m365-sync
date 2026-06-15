import hashlib
import hmac
import json
import logging
import os

import azure.functions as func

from src.functions.onGroupMemberAdded import run as on_member_added
from src.functions.onGroupMemberRemoved import run as on_member_removed
from src.functions.onGroupCreated import run as on_group_created
from src.functions.onGroupDeleted import run as on_group_deleted

logger = logging.getLogger(__name__)

EVENT_HANDLERS = {
    "group.user_membership.add":    on_member_added,
    "group.user_membership.remove": on_member_removed,
    "group.lifecycle.create":       on_group_created,
    "group.lifecycle.delete":       on_group_deleted,
}


def verify_okta_signature(req: func.HttpRequest) -> bool:
    secret = os.environ.get("OKTA_WEBHOOK_SECRET", "")
    signature = req.headers.get("x-okta-verification-challenge", "")
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), req.get_body(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def main(req: func.HttpRequest) -> func.HttpResponse:
    challenge = req.headers.get("x-okta-verification-challenge")
    if challenge:
        return func.HttpResponse(
            json.dumps({"verification": challenge}),
            mimetype="application/json"
        )

    if not verify_okta_signature(req):
        logger.warning("Invalid Okta webhook signature")
        return func.HttpResponse("Unauthorized", status_code=401)

    try:
        payload = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    for event in payload.get("data", {}).get("events", []):
        event_type = event.get("eventType")
        handler = EVENT_HANDLERS.get(event_type)
        if handler:
            logger.info(f"Handling event: {event_type}")
            handler(event)
        else:
            logger.info(f"No handler for event type: {event_type}")

    return func.HttpResponse("OK", status_code=200)
