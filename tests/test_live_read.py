import unittest
import sys
import os

sys.path.insert(0, "/mnt/datos/proyectos/workspace-assistant")
sys.path.insert(0, "/home/hermes/.hermes/workspace-assistant")

from workspace_assistant import WorkspaceAssistant

class TestLiveReadIntegrations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assistant = WorkspaceAssistant()

    def test_gmail_profile(self):
        profile = self.assistant.gmail.get_profile()
        self.assertIn("emailAddress", profile)
        self.assertIn("messagesTotal", profile)

    def test_calendar_freebusy(self):
        fb = self.assistant.calendar.query_freebusy(
            time_min="2026-08-30T00:00:00Z",
            time_max="2026-08-31T00:00:00Z"
        )
        self.assertIn("primary", fb)

    def test_tasks_list(self):
        lists = self.assistant.tasks.list_tasklists()
        self.assertIsInstance(lists, list)

    def test_drive_list(self):
        files = self.assistant.drive.list_files(page_size=1)
        self.assertIsInstance(files, list)

if __name__ == "__main__":
    unittest.main()
