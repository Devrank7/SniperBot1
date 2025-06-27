from telethon import errors, TelegramClient


async def auth_client(client: TelegramClient):
    if await client.is_user_authorized():
        print('Ви вже авторизовані!')
        return client

    print("Потрібна авторизація...")
    try:
        number = input('Введіть номер телефону з Telegram, наприклад +380XXXXXXXXX: ')
        await client.send_code_request(number)
        code = input('Введіть код, який прийшов у Telegram: ')
        await client.sign_in(phone=number, code=code)
    except errors.SessionPasswordNeededError:
        pwd = input('Введіть пароль двофакторної автентифікації: ')
        await client.sign_in(password=pwd)

    print('Успішна авторизація!')
    return client