class TaskQueue:
    def __init__(self, tasks=None):
        self._tasks = list(tasks or [])

    def add(self, task):
        self._tasks.append(task)

    def all(self):
        return self._tasks

    def set_status(self, task_id, status, result=None, error=None):
        for task in self._tasks:
            if task.get("id") == task_id:
                task["status"] = status
                if result is not None:
                    task["result"] = result
                if error is not None:
                    task["error"] = error
                return task
        return None
