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
        data_user = input("Введіть час і повідомлення через кому, наприклад (14:30, привіт): ")
        try:
            time_to_send, message = map(str.strip, data_user.split(",", 1))
            datetime.strptime(time_to_send, "%H:%M")  # Валідація часу
            data_dict[time_to_send] = message  # Замінює, якщо час вже є
        except ValueError:
            print(Fore.RED + 'Невірний формат. Використовуйте "HH:MM, повідомлення"' + Style.RESET_ALL)
            continue
        is_end = input("Додати ще одну мітку часу з повідомленням? (yes/start): ") == 'start'

    return list(data_dict.items())


def schedule_daily_messages(client: TelegramClient, data: list[tuple[str, str]]):
    for time_str, message in data:
        hour, minute = map(int, time_str.split(":"))
        trigger = CronTrigger(hour=hour, minute=minute, second=0)
        task = TaskSniper(client, message)
        scheduler.add_job(task.run, trigger=trigger)
        print(f"Заплановано: '{message}' щодня о {hour:02d}:{minute:02d}.00.000")


async def main():
    print("Запуск планувального скрипта з миттєвою відправкою за часом...")
    client = TelegramClient('sessions/session', API_ID, API_HASH)
    await client.connect()
    try:
        client = await auth_client(client)
        data: list[tuple[str, str]] = get_data_snip()
        schedule_daily_messages(client, data)
        scheduler.start()

        print("Планувальний скрипт запущено. Очікуємо на щоденну відправку повідомлень у зазначений час...")
        while True:
            await asyncio.sleep(60)
    finally:
        await client.disconnect()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Програму зупинено.")
