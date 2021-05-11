

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

print(
    """Vaya a my.telegram.org
Inicie sesión con su cuenta de Telegram
Haga clic en Herramientas de desarrollo de API
Cree una nueva aplicación, ingresando los detalles requeridos"""
)
APP_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    print(client.session.save())
    client.send_message("me", client.session.save())
