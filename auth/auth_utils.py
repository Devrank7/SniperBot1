from telethon import errors, TelegramClient


async def auth_client(client: TelegramClient):
    if await client.is_user_authorized():
        print('Уже авторизованы!')
        return client
    print("Нужно авторизоваться...")
    try:
        number = input('Введите номер телефона из телеграма, например +380XXXXXXXXX: ')
        # Если это первый вход, Telethon отправит код:
        await client.send_code_request(number)
        code = input('Введите код, который пришел Telegram: ')
        await client.sign_in(phone=number, code=code)
    except errors.SessionPasswordNeededError:
        # Требуется второй фактор — пароль от облака
        pwd = input('Введите пароль двухфакторной аутентификации: ')
        await client.sign_in(password=pwd)

    print('Вы успешно авторизованы!')
    return client