from ..guardrails import SecurityPolicy

class DriveService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_drive_service()
        return self._service

    def list_files(self, page_size: int = 20, query: str = None):
        q = "trashed = false"
        if query:
            q = f"({q}) and ({query})"
        res = self.service.files().list(pageSize=page_size, q=q, fields="files(id, name, mimeType, modifiedTime)").execute()
        files = res.get("files", [])
        self.audit.log("drive.list_files", "files", "SUCCESS", details={"count": len(files)})
        return files

    def get_file_metadata(self, file_id: str):
        meta = self.service.files().get(fileId=file_id, fields="id, name, mimeType, parents, owners, permissions").execute()
        self.audit.log("drive.get_metadata", f"file:{file_id}", "SUCCESS")
        return meta

    def create_folder(self, name: str, parent_id: str = None):
        body = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parent_id:
            body["parents"] = [parent_id]
        folder = self.service.files().create(body=body, fields="id, name").execute()
        self.audit.log("drive.create_folder", f"folder:{folder.get('id')}", "SUCCESS", details={"name": name})
        return folder

    def move_to_trash(self, file_id: str, confirmed: bool = False):
        SecurityPolicy.enforce("drive.trash", confirmed=confirmed, details={"file_id": file_id})
        res = self.service.files().update(fileId=file_id, body={"trashed": True}).execute()
        self.audit.log("drive.trash", f"file:{file_id}", "SUCCESS")
        return res

    def permanent_delete(self, file_id: str):
        SecurityPolicy.enforce("drive.permanent_delete")

    def transfer_ownership(self, file_id: str, new_owner_email: str):
        SecurityPolicy.enforce("drive.transfer_ownership")

    def share_publicly(self, file_id: str):
        SecurityPolicy.enforce("drive.public_share")
