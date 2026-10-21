import json
import logging
import os
import sys
from datetime import datetime, timezone

class AuditLogger:
    def __init__(self, log_path: str = "/mnt/datos/proyectos/workspace-assistant/audit.log"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
        self.logger = logging.getLogger("workspace_assistant_audit")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)

    def log(self, action: str, resource: str, result: str, caller: str = "assistant", details: dict = None):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "resource": resource,
            "caller": caller,
            "result": result,
            "details": details or {}
        }
        # Redact any accidental tokens or full sensitive bodies
        sanitized = self._sanitize(entry)
        self.logger.info(json.dumps(sanitized))
        return sanitized

    def _sanitize(self, obj):
        if isinstance(obj, dict):
            clean = {}
            for k, v in obj.items():
                if k.lower() in ("token", "secret", "password", "authorization", "access_token", "refresh_token", "body_full"):
                    clean[k] = "[REDACTED]"
                else:
                    clean[k] = self._sanitize(v)
            return clean
        elif isinstance(obj, list):
            return [self._sanitize(elem) for elem in obj]
        return obj
