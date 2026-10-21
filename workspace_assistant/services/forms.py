from ..guardrails import SecurityPolicy

class FormsService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_forms_service()
        return self._service

    def get_form(self, form_id: str):
        form = self.service.forms().get(formId=form_id).execute()
        self.audit.log("forms.get_form", f"form:{form_id}", "SUCCESS")
        return form

    def list_responses(self, form_id: str):
        res = self.service.forms().responses().list(formId=form_id).execute()
        responses = res.get("responses", [])
        self.audit.log("forms.list_responses", f"form:{form_id}", "SUCCESS", details={"count": len(responses)})
        return responses
