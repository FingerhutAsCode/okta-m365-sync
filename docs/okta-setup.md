# Okta Setup

## 1. Create an API Token
Okta Admin → Security → API → Tokens → Create Token

## 2. Configure an Event Hook
Okta Admin → Workflow → Event Hooks → Add Event Hook

- **Name:** M365 Group Sync
- **URL:** `https://<your-function-app>.azurewebsites.net/api/webhook`
- **Events to subscribe:**
  - `group.user_membership.add`
  - `group.user_membership.remove`
  - `group.lifecycle.create`
  - `group.lifecycle.delete`

## 3. Verify the Hook
Okta sends a verification challenge — the receiver handles this automatically.
