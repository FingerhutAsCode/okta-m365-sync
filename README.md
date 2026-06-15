# okta-m365-sync

A lightweight, open-source solution for syncing Okta group membership to Microsoft 365 Groups and Distribution Lists via Okta Event Hooks and the Microsoft Graph API.

## Problem

Okta's native Group Push only syncs to Entra ID security groups. Organizations that need M365 Groups or Exchange Distribution Lists kept in sync with Okta groups have no simple open-source solution — this fills that gap.

## Assumptions

Knowledge of Azure, Okta, and M365 Administration

## How It Works

1. Okta fires an Event Hook on group membership changes
2. An Azure Function receives, validates, and routes the event
3. The appropriate handler calls the Microsoft Graph API to mirror the change in M365

## Supported Events

| Okta Event | Action |
|---|---|
| `group.user_membership.add` | Add user to M365 Group / Distribution List |
| `group.user_membership.remove` | Remove user from M365 Group / Distribution List |
| `group.lifecycle.create` | Create corresponding M365 Group / Distribution List |
| `group.lifecycle.delete` | Delete corresponding M365 Group / Distribution List |

## Quick Start

### Prerequisites
- Azure subscription
- Okta tenant with Event Hooks available
- Python 3.11+
- Azure Functions Core Tools
- Azure CLI

### Local Development
```bash
git clone https://github.com/yourusername/okta-m365-sync.git
cd okta-m365-sync
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
# Fill in .env values
func start
```

### Deploy to Azure
Push to `main` — GitHub Actions handles the rest.
See [Azure Setup](docs/azure-setup.md) and [Okta Setup](docs/okta-setup.md).

## Configuration

Copy `.env.example` to `.env` and populate values.
Group mappings are managed in `config/group_mappings.json`.

## Project Structure

```
├── .github/workflows/   # CI/CD pipeline
├── src/
│   ├── receiver/        # Webhook entry point + signature validation
│   ├── functions/       # One handler per Okta event type
│   └── shared/          # Graph client, mapping helpers, logger
├── infra/               # Bicep infrastructure as code
├── config/              # Group mapping configuration
├── tests/               # Test scaffolding
└── docs/                # Setup guides and architecture
```

## Contributing

PRs welcome. Please add tests for new event handlers.

## License

MIT
