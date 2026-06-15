# Architecture

## Overview

```
Okta Event Hook
      │
      ▼
Azure Function (HTTP Trigger)
  └── Signature Validation
  └── Event Router
        ├── group.user_membership.add    → onGroupMemberAdded
        ├── group.user_membership.remove → onGroupMemberRemoved
        ├── group.lifecycle.create       → onGroupCreated
        └── group.lifecycle.delete       → onGroupDeleted
                    │
                    ▼
            Microsoft Graph API
                    │
          ┌─────────┴──────────┐
     M365 Groups        Distribution Lists
```

## Components

- **Webhook Receiver** — validates Okta signatures, routes events
- **Event Handlers** — one per Okta event type
- **Graph Client** — shared MSAL-authenticated Graph API wrapper
- **Group Mappings** — JSON config mapping Okta group IDs to M365 group IDs
- **Bicep Infra** — Function App, Storage Account, App Service Plan

## Environment Variables

See `.env.example` for full reference.
