import unittest
import sys
import os

sys.path.insert(0, "/mnt/datos/proyectos/workspace-assistant")
sys.path.insert(0, "/home/hermes/.hermes/workspace-assistant")

from workspace_assistant.guardrails import (
    SecurityPolicy,
    BlockedOperationError,
    ConfirmationRequiredError,
    BLOCKED_OPERATIONS,
    CONFIRMATION_REQUIRED_OPERATIONS
)
from workspace_assistant.audit import AuditLogger

class TestSecurityGuardrails(unittest.TestCase):
    def test_blocked_operations(self):
        for op in BLOCKED_OPERATIONS:
            with self.assertRaises(BlockedOperationError):
                SecurityPolicy.enforce(op)

    def test_confirmation_required_unconfirmed(self):
        for op in CONFIRMATION_REQUIRED_OPERATIONS:
            with self.assertRaises(ConfirmationRequiredError):
                SecurityPolicy.enforce(op, confirmed=False)

    def test_confirmation_required_confirmed(self):
        for op in CONFIRMATION_REQUIRED_OPERATIONS:
            self.assertTrue(SecurityPolicy.enforce(op, confirmed=True))

    def test_audit_logger_sanitization(self):
        logger = AuditLogger(log_path="/mnt/datos/proyectos/workspace-assistant/test_audit.log")
        entry = logger.log(
            action="test_action",
            resource="test_resource",
            result="SUCCESS",
            details={
                "access_token": "secret_token_value",
                "normal_field": "safe_value"
            }
        )
        self.assertEqual(entry["details"]["access_token"], "[REDACTED]")
        self.assertEqual(entry["details"]["normal_field"], "safe_value")

if __name__ == "__main__":
    unittest.main()
