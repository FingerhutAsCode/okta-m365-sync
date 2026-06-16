import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.function_name("OktaEventHook")
@app.route(route="okta/event-hook", methods=["GET", "POST"])
def okta_event_hook(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Okta event hook triggered")

    # Handle Okta's one-time verification challenge
    if req.method == "GET":
        challenge = req.params.get("challenge")
        if challenge:
            return func.HttpResponse(
                json.dumps({"verification": challenge}),
                mimetype="application/json",
                status_code=200
            )

    # Handle incoming events
    try:
        payload = req.get_json()
        events = payload.get("data", {}).get("events", [])

        for event in events:
            event_type = event.get("eventType")
            logging.info(f"Received event: {event_type}")

            if event_type == "group.user_membership.add":
                # TODO: call Graph API to add user to M365 group
                pass
            elif event_type == "group.user_membership.remove":
                # TODO: call Graph API to remove user from M365 group
                pass

        return func.HttpResponse("OK", status_code=200)

    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return func.HttpResponse("Bad Request", status_code=400)