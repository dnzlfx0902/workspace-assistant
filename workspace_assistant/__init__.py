"""
workspace-assistant: Google Workspace integration package with security guardrails and audit logging.
"""

from .assistant import WorkspaceAssistant
from .guardrails import BlockedOperationError, ConfirmationRequiredError
from .audit import AuditLogger

__all__ = [
    "WorkspaceAssistant",
    "BlockedOperationError",
    "ConfirmationRequiredError",
    "AuditLogger",
]
