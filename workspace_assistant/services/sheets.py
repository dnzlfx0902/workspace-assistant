from ..guardrails import SecurityPolicy

class SheetsService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_sheets_service()
        return self._service

    def create_spreadsheet(self, title: str):
        sheet = self.service.spreadsheets().create(body={"properties": {"title": title}}).execute()
        self.audit.log("sheets.create", f"sheet:{sheet.get('spreadsheetId')}", "SUCCESS", details={"title": title})
        return sheet

    def get_values(self, spreadsheet_id: str, range_name: str):
        res = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        self.audit.log("sheets.get_values", f"sheet:{spreadsheet_id}/range:{range_name}", "SUCCESS")
        return res.get("values", [])

    def append_rows(self, spreadsheet_id: str, range_name: str, values: list):
        body = {"values": values}
        res = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        self.audit.log("sheets.append_rows", f"sheet:{spreadsheet_id}/range:{range_name}", "SUCCESS", details={"rows": len(values)})
        return res

    def update_values(self, spreadsheet_id: str, range_name: str, values: list, confirmed: bool = False):
        total_cells = sum(len(row) for row in values) if values else 0
        if total_cells > 50:
            SecurityPolicy.enforce("sheets.batch_overwrite_large", confirmed=confirmed, details={"spreadsheet_id": spreadsheet_id, "cells": total_cells})

        body = {"values": values}
        res = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        self.audit.log("sheets.update_values", f"sheet:{spreadsheet_id}/range:{range_name}", "SUCCESS", details={"cells": total_cells})
        return res
