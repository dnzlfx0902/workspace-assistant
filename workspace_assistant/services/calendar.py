from datetime import datetime, timezone
from ..guardrails import SecurityPolicy

class CalendarService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_calendar_service()
        return self._service

    def list_events(self, calendar_id: str = "primary", max_results: int = 10, time_min: str = None):
        now = time_min or datetime.now(timezone.utc).isoformat()
        res = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        items = res.get("items", [])
        self.audit.log("calendar.list_events", f"calendar:{calendar_id}", "SUCCESS", details={"count": len(items)})
        return items

    def query_freebusy(self, time_min: str, time_max: str, calendar_ids: list = None):
        c_ids = calendar_ids or ["primary"]
        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": cid} for cid in c_ids]
        }
        res = self.service.freebusy().query(body=body).execute()
        self.audit.log("calendar.query_freebusy", "calendars", "SUCCESS", details={"calendars": c_ids})
        return res.get("calendars", {})

    def create_event(self, summary: str, start_time: str, end_time: str, attendees: list = None, confirmed: bool = False):
        has_external_attendees = attendees and len(attendees) > 0
        if has_external_attendees:
            SecurityPolicy.enforce("calendar.invite_external", confirmed=confirmed, details={"summary": summary, "attendees": attendees})

        event_body = {
            "summary": summary,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time}
        }
        if attendees:
            event_body["attendees"] = [{"email": a} for a in attendees]

        created = self.service.events().insert(calendarId="primary", body=event_body).execute()
        self.audit.log("calendar.create_event", f"event:{created.get('id')}", "SUCCESS", details={"summary": summary})
        return created

    def delete_event(self, event_id: str, is_shared: bool = False, confirmed: bool = False):
        if is_shared:
            SecurityPolicy.enforce("calendar.cancel_shared_event", confirmed=confirmed, details={"event_id": event_id})
        res = self.service.events().delete(calendarId="primary", eventId=event_id).execute()
        self.audit.log("calendar.delete_event", f"event:{event_id}", "SUCCESS")
        return res
