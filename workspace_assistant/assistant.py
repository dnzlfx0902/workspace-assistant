"""
Main WorkspaceAssistant Orchestrator Class
"""

import sys
import os

# Add sysadmin handoff directory to path if needed
SYSADMIN_HANDOFF_DIR = "/home/hermes/.hermes/workspace-assistant"
if SYSADMIN_HANDOFF_DIR not in sys.path:
    sys.path.insert(0, SYSADMIN_HANDOFF_DIR)

from client import WorkspaceClientFactory
from .audit import AuditLogger
from .services.gmail import GmailService
from .services.calendar import CalendarService
from .services.tasks import TasksService
from .services.drive import DriveService
from .services.docs import DocsService
from .services.sheets import SheetsService
from .services.slides import SlidesService
from .services.forms import FormsService

class WorkspaceAssistant:
    def __init__(self, token_path: str = None, audit_log_path: str = None):
        if token_path:
            self.factory = WorkspaceClientFactory(token_path=token_path)
        else:
            self.factory = WorkspaceClientFactory()
        
        self.audit = AuditLogger(log_path=audit_log_path or "/mnt/datos/proyectos/workspace-assistant/audit.log")
        
        # Initialize modular services
        self.gmail = GmailService(self.factory, self.audit)
        self.calendar = CalendarService(self.factory, self.audit)
        self.tasks = TasksService(self.factory, self.audit)
        self.drive = DriveService(self.factory, self.audit)
        self.docs = DocsService(self.factory, self.audit)
        self.sheets = SheetsService(self.factory, self.audit)
        self.slides = SlidesService(self.factory, self.audit)
        self.forms = FormsService(self.factory, self.audit)
