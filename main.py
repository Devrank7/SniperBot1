import asyncio
import os
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from colorama import Style, Fore
from dotenv import load_dotenv
from telethon import TelegramClient

from auth.auth_utils import auth_client
from tasks.scheduler import scheduler
from tasks.tasks import TaskSniper

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')


def get_data_snip() -> list[tuple[str, str]]:
    is_end = False
    data_dict: dict[str, str] = {}

    while not is_end:
        data_user = input("Введите время и сообщение для отправки через запятую, например (14:30, привет): ")
        try:
            time_to_send, message = map(str.strip, data_user.split(",", 1))
            datetime.strptime(time_to_send, "%H:%M")  # Валидация времени
            data_dict[time_to_send] = message  # Заменит, если уже было такое время
        except ValueError:
            print(Fore.RED + 'Неверный формат. Используйте "HH:MM, сообщение"' + Style.RESET_ALL)
            if len(data_dict) == 0:
                continue
        is_end = input("Добавить еще временную метку с сообщение? (yes/start): ") == 'start'

    return list(data_dict.items())


def schedule_daily_messages(client: TelegramClient, data: list[tuple[str, str]]):
    for time_str, message in data:
        hour, minute = map(int, time_str.split(":"))
        trigger = CronTrigger(hour=hour, minute=minute, second=0)
        task = TaskSniper(client, message)
        scheduler.add_job(task.run, trigger=trigger)
        print(f"Запланировано: '{message}' каждый день в {hour:02d}:{minute:02d}.00.000")


async def main():
    print("Запуск планировщика с моментальным отправлением по времени...")
    client = TelegramClient('sessions/session', API_ID, API_HASH)
    await client.connect()
    try:
        client = await auth_client(client)
        data: list[tuple[str, str]] = get_data_snip()
        schedule_daily_messages(client, data)
        scheduler.start()

        print("Планировщик запущен. Ожидаем моментальной ежедневной отправки сообщений в указанное время...")
        while True:
            await asyncio.sleep(60)
    finally:
        await client.disconnect()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Программа остановлена.")
