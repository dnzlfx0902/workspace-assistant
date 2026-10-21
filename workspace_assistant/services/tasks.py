from ..guardrails import SecurityPolicy

class TasksService:
    def __init__(self, factory, audit_logger):
        self.factory = factory
        self.audit = audit_logger
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = self.factory.get_tasks_service()
        return self._service

    def list_tasklists(self, max_results: int = 10):
        res = self.service.tasklists().list(maxResults=max_results).execute()
        lists = res.get("items", [])
        self.audit.log("tasks.list_tasklists", "tasklists", "SUCCESS", details={"count": len(lists)})
        return lists

    def list_tasks(self, tasklist_id: str = "@default", max_results: int = 20):
        res = self.service.tasks().list(tasklist=tasklist_id, maxResults=max_results).execute()
        items = res.get("items", [])
        self.audit.log("tasks.list_tasks", f"tasklist:{tasklist_id}", "SUCCESS", details={"count": len(items)})
        return items

    def create_task(self, title: str, notes: str = None, due: str = None, tasklist_id: str = "@default"):
        body = {"title": title}
        if notes:
            body["notes"] = notes
        if due:
            body["due"] = due
        task = self.service.tasks().insert(tasklist=tasklist_id, body=body).execute()
        self.audit.log("tasks.create_task", f"task:{task.get('id')}", "SUCCESS", details={"title": title})
        return task

    def update_task_status(self, task_id: str, status: str = "completed", tasklist_id: str = "@default"):
        task = self.service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        task["status"] = status
        updated = self.service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
        self.audit.log("tasks.update_status", f"task:{task_id}", "SUCCESS", details={"status": status})
        return updated

    def delete_task(self, task_id: str, tasklist_id: str = "@default", confirmed: bool = False):
        SecurityPolicy.enforce("tasks.delete", confirmed=confirmed, details={"task_id": task_id})
        res = self.service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
        self.audit.log("tasks.delete_task", f"task:{task_id}", "SUCCESS")
        return res
