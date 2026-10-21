"""
Security Guardrails for Google Workspace Assistant
"""

class BlockedOperationError(Exception):
    """Raised when an operation is permanently prohibited by security policy."""
    pass

class ConfirmationRequiredError(Exception):
    """Raised when an operation requires explicit user confirmation before execution."""
    pass

BLOCKED_OPERATIONS = {
    "drive.permanent_delete",
    "drive.transfer_ownership",
    "drive.public_share",
    "drive.domain_share",
    "admin.manage_users",
    "admin.manage_groups",
    "apps_script.execute",
    "gmail.delete_permanent",
    "gmail.delegate_account"
}

CONFIRMATION_REQUIRED_OPERATIONS = {
    "gmail.send",
    "calendar.invite_external",
    "calendar.cancel_shared_event",
    "tasks.delete",
    "drive.trash",
    "drive.move_outside_allowlist",
    "sheets.batch_overwrite_large",
    "docs.replace_entire_document",
    "forms.submit_response"
}

class SecurityPolicy:
    @staticmethod
    def enforce(operation: str, confirmed: bool = False, details: dict = None):
        if operation in BLOCKED_OPERATIONS:
            raise BlockedOperationError(
                f"Operation '{operation}' is BLOCKED by workspace security policy and cannot be executed."
            )
        if operation in CONFIRMATION_REQUIRED_OPERATIONS and not confirmed:
            raise ConfirmationRequiredError(
                f"Operation '{operation}' requires explicit user confirmation. Re-run with confirmed=True. Details: {details or {}}"
            )
        return True
