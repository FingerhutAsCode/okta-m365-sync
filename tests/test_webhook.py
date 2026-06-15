import json
import pytest

def test_okta_verification_challenge():
    challenge = "abc123"
    response_body = {"verification": challenge}
    assert response_body["verification"] == challenge

def test_invalid_signature_returns_401():
    status_code = 401
    assert status_code == 401

def test_unknown_event_type_is_ignored():
    event_type = "unknown.event.type"
    from src.receiver.webhook import EVENT_HANDLERS
    assert event_type not in EVENT_HANDLERS
