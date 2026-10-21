import base64
from email.mime.text import MIMEText
from ..guardrails import SecurityPolicy

class GmailService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_gmail_service()
        return self._service

    def get_profile(self):
        profile = self.service.users().getProfile(userId="me").execute()
        self.audit.log("gmail.get_profile", "users/me", "SUCCESS")
        return {
            "emailAddress": profile.get("emailAddress"),
            "messagesTotal": profile.get("messagesTotal"),
            "threadsTotal": profile.get("threadsTotal")
        }

    def list_messages(self, query: str = "", max_results: int = 10):
        res = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
        messages = res.get("messages", [])
        self.audit.log("gmail.list_messages", f"query:{query}", "SUCCESS", details={"count": len(messages)})
        return messages

    def get_message(self, message_id: str):
        msg = self.service.users().messages().get(userId="me", id=message_id, format="metadata").execute()
        self.audit.log("gmail.get_message", f"message:{message_id}", "SUCCESS")
        return msg

    def create_draft(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        draft = self.service.users().drafts().create(
            userId="me",
            body={"message": {"raw": raw}}
        ).execute()
        self.audit.log("gmail.create_draft", f"draft:{draft.get('id')}", "SUCCESS", details={"to": to, "subject": subject})
        return draft

    def send_message(self, to: str, subject: str, body: str, confirmed: bool = False):
        SecurityPolicy.enforce("gmail.send", confirmed=confirmed, details={"to": to, "subject": subject})
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        sent = self.service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()
        self.audit.log("gmail.send", f"message:{sent.get('id')}", "SUCCESS", details={"to": to, "subject": subject})
        return sent

    def trash_message(self, message_id: str):
        res = self.service.users().messages().trash(userId="me", id=message_id).execute()
        self.audit.log("gmail.trash_message", f"message:{message_id}", "SUCCESS")
        return res

    def delete_message_permanent(self, message_id: str):
        SecurityPolicy.enforce("gmail.delete_permanent")
