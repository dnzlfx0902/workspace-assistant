from ..guardrails import SecurityPolicy

class SlidesService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_slides_service()
        return self._service

    def create_presentation(self, title: str):
        pres = self.service.presentations().create(body={"title": title}).execute()
        self.audit.log("slides.create", f"presentation:{pres.get('presentationId')}", "SUCCESS", details={"title": title})
        return pres

    def get_presentation(self, presentation_id: str):
        pres = self.service.presentations().get(presentationId=presentation_id).execute()
        self.audit.log("slides.get", f"presentation:{presentation_id}", "SUCCESS")
        return pres

    def add_slide(self, presentation_id: str, insertion_index: int = None):
        requests = [{
            "createSlide": {
                "insertionIndex": insertion_index
            }
        }]
        res = self.service.presentations().batchUpdate(presentationId=presentation_id, body={"requests": requests}).execute()
        self.audit.log("slides.add_slide", f"presentation:{presentation_id}", "SUCCESS")
        return res
