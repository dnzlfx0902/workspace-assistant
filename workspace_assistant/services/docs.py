from ..guardrails import SecurityPolicy

class DocsService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_docs_service()
        return self._service

    def create_document(self, title: str):
        doc = self.service.documents().create(body={"title": title}).execute()
        self.audit.log("docs.create", f"doc:{doc.get('documentId')}", "SUCCESS", details={"title": title})
        return doc

    def get_document(self, document_id: str):
        doc = self.service.documents().get(documentId=document_id).execute()
        self.audit.log("docs.get", f"doc:{document_id}", "SUCCESS")
        return doc

    def append_text(self, document_id: str, text: str):
        requests = [{
            "insertText": {
                "endOfSegmentLocation": {},
                "text": text
            }
        }]
        res = self.service.documents().batchUpdate(documentId=document_id, body={"requests": requests}).execute()
        self.audit.log("docs.append_text", f"doc:{document_id}", "SUCCESS", details={"length": len(text)})
        return res
