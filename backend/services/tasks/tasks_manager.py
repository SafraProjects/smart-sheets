import asyncio
from typing import Callable, Any, Dict, Optional
import uuid
from datetime import timedelta, datetime


class TaskManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.task_queue = asyncio.Queue()
        self.running_tasks: Dict[str, asyncio.Task] = {}

        # הרץ את מנהל המשימות
        asyncio.create_task(self.run())

    async def add_task(self, task: Callable, *args: Any, **kwargs: Any) -> asyncio.Event:
        task_event = asyncio.Event()
        await self.task_queue.put((task, args, kwargs, task_event))
        print("Task added to the queue.")
        return task_event

    async def add_scheduled_task(self, task: Callable, start_time: datetime, end_time: datetime, interval: timedelta) -> None:
        while True:
            now = datetime.now()
            if now < start_time:
                # המתן עד זמן ההתחלה
                await asyncio.sleep((start_time - now).total_seconds())
            elif now > end_time:
                print("End time reached. Stopping scheduled task.")
                break  # אם הגענו לסוף הזמן, מפסיקים את המשימה

            task_event = await self.add_task(task)  # הוסף את המשימה
            await asyncio.sleep(interval.total_seconds())  # המתן עד לתאריך הבא

    async def run(self):
        while True:
            # מחכה שתהיה משימה בתור
            task, args, kwargs, task_event = await self.task_queue.get()

            # הודעת התחלת משימה
            task_id = str(uuid.uuid4())
            print(f"Starting a new task with ID: {task_id}...")

            async def task_wrapper():
                result = await task(*args, **kwargs)  # הרץ את המשימה
                print(f"Task {task_id} completed.")  # הודעת סיום משימה
                # הודעה למערכת הקדמית
                await self.notify_frontend(task_id, result)

            task_future = asyncio.create_task(task_wrapper())
            self.running_tasks[task_id] = task_future  # הוסף את המשימה לרשימה

            # ניהול סיום המשימות
            task_future.add_done_callback(
                lambda fut: self.task_completed(task_id, task_event))

    async def notify_frontend(self, task_id: str, result):
        # כאן תוכל להוסיף קוד לשליחת הודעות ל-Frontend
        print(
            f"Notification sent: Task {task_id} completed. and the result is", result)

    def task_completed(self, task_id: str, task_event: asyncio.Event):
        print(f"Task {task_id} has been marked as completed.")
        task_event.set()  # מעיר את האירוע
        del self.running_tasks[task_id]  # הסר את המשימה מהרשימה

    async def wait_for_task(self, task_event: asyncio.Event):
        await task_event.wait()
        print("Task completed successfully!")

# פונקציה שמחזירה מופע של מנהל המשימות


def get_task_manager() -> TaskManager:
    return TaskManager()
