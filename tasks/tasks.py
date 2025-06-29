import asyncio
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

class TaskSniperQuik(TaskExecute):
    def __init__(self, client: TelegramClient, message: str, quik_mode = True, entity = -1002268902235):
        self.client = client
        self.message = message
        self.entity = entity
        self.quik_mode = quik_mode

    async def run(self):
        await asyncio.sleep(0.88)
        if self.quik_mode:
            await asyncio.sleep(0.92)
        print(f"Відправляємо повідомлення {datetime.now().strftime("%H:%M:%S.%f")}")
        await self.client.send_message(self.entity, self.message)
        print(f"Повідомлення '{self.message}' відправлено! {datetime.now().strftime("%H:%M:%S.%f")}")