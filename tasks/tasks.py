from abc import ABC, abstractmethod

from telethon import TelegramClient


class TaskExecute(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError

class TaskSniper(TaskExecute):


    def __init__(self, client: TelegramClient, message: str, entity = -4842758811) -> None:
        self.client = client
        self.message = message
        self.entity = entity

    async def run(self):
        await self.client.send_message(self.entity, self.message)
        print(f"Повідомлення '{self.message}' відправлено!")