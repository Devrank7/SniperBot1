from abc import ABC, abstractmethod
from datetime import datetime

from telethon import TelegramClient


class TaskExecute(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError

class TaskSniper(TaskExecute):


    def __init__(self, client: TelegramClient, message: str, entity = -1002268902235) -> None:
        self.client = client
        self.message = message
        self.entity = entity

    async def run(self):
        print(f"Відправляємо повідомлення {datetime.now().strftime("%H:%M:%S.%f")}")
        await self.client.send_message(self.entity, self.message)
        print(f"Повідомлення '{self.message}' відправлено! {datetime.now().strftime("%H:%M:%S.%f")}")