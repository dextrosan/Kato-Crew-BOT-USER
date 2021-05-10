

"""
✅ Comandos by: @Dextrov -

• `{i}mute <reply to msg/ user id>`
    Silenciar al usuario en el chat actual.

• `{i}unmute <reply to msg/ user id>`
    Dejar de silenciar al usuario en el chat actual.

• `{i}dmute <reply to msg/ user id>`
    Silenciar al usuario en el chat actual eliminando mensajes.

• `{i}undmute <reply to msg/ use id>`
    Activa el silencio del usuario silenciado en el chat actual.

• `{i}tmute <time> <reply to msg/ use id>`
    time - m- minutos
           h- horas
           d- dias
    Silenciar al usuario en el chat actual con el tiempo.
"""


from pyUltroid.functions.all import ban_time
from pyUltroid.functions.mute_db import is_muted, mute, unmute
from telethon import events

from . import *


@ultroid_bot.on(events.NewMessage(incoming=True))
async def watcher(event):
    if is_muted(f"{event.sender_id}_{event.chat_id}"):
        await event.delete()


@ultroid_cmd(
    pattern="dmute ?(.*)",
)
async def startmute(event):
    xx = await eor(event, "`Muting...`")
    input = event.pattern_match.group(1)
    private = False
    if event.is_private:
        private = True
    if input:
        if input.isdigit():
            try:
                userid = input
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await event.client.get_entity(input)).id
    elif event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(xx, "`Responder a un usuario o añadir su userid.`", time=5)
    chat_id = event.chat_id
    chat = await event.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is True:
            pass
        else:
            return await eor(xx, "`Sin derechos de administrador adecuados...`", time=5)
    elif "creator" in vars(chat):
        pass
    elif private:
        pass
    else:
        return await eod(xx, "`Sin derechos de administrador adecuados...`", time=5)
    if is_muted(f"{userid}_{chat_id}"):
        return await eod(xx, "`Este usuario ya está silenciado en este chat..`", time=5)
    try:
        mute(f"{userid}_{chat_id}")
        await eod(xx, "`Silenciado con éxito...`", time=3)
    except Exception as e:
        await eod(xx, "Error: " + f"`{str(e)}`")


@ultroid_cmd(
    pattern="undmute ?(.*)",
)
async def endmute(event):
    xx = await eor(event, "`Desmuteado...`")
    private = False
    input = event.pattern_match.group(1)
    if event.is_private:
        private = True
    if input:
        if input.isdigit():
            try:
                userid = input
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await event.client.get_entity(input)).id
    elif event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(xx, "`Responder a un usuario o añadir su userid.`", time=5)
    chat_id = event.chat_id
    if not is_muted(f"{userid}_{chat_id}"):
        return await eod(xx, "`Este usuario no está silenciado en este chat..`", time=3)
    try:
        unmute(f"{userid}_{chat_id}")
        await eod(xx, "`Desactivado correctamente...`", time=3)
    except Exception as e:
        await eod(xx, "Error: " + f"`{str(e)}`")


@ultroid_cmd(
    pattern="tmute",
    groups_only=True,
)
async def _(e):
    xx = await eor(e, "`Muting...`")
    huh = e.text.split(" ")
    try:
        tme = huh[1]
    except BaseException:
        return await eod(xx, "`¿Es hora de silenciar?`", time=5)
    try:
        input = huh[2]
    except BaseException:
        pass
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await event.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Responder a alguien o usar su id...`", time=3)
    if userid == ultroid_bot.uid:
        return await eod(xx, "`No puedo silenciarme.`", time=3)
    try:
        bun = await ban_time(xx, tme)
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=bun,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Silenciado con exito` [{name}](tg://user?id={userid}) `En {chat.title} por {tme}`",
            time=5,
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")


@ultroid_cmd(
    pattern="unmute ?(.*)",
    groups_only=True,
)
async def _(e):
    xx = await eor(e, "`Unmuting...`")
    input = e.pattern_match.group(1)
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await e.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Responder a alguien o usar su id...`", time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=True,
        )
        await eod(
            xx,
            f"`Desmuteado correctamente` [{name}](tg://user?id={userid}) `in {chat.title}`",
            time=5,
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")


@ultroid_cmd(
    pattern="mute ?(.*)",
    groups_only=True,
)
async def _(e):
    xx = await eor(e, "`Muting...`")
    input = e.pattern_match.group(1)
    chat = await e.get_chat()
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        if input.isdigit():
            try:
                userid = input
                name = (await e.client.get_entity(userid)).first_name
            except ValueError as x:
                return await xx.edit(str(x))
        else:
            userid = (await e.client.get_entity(input)).id
            name = (await e.client.get_entity(userid)).first_name
    else:
        return await eod(xx, "`Responder a alguien o usar su id...`", time=3)
    if userid == ultroid_bot.uid:
        return await eod(xx, "`No puedo silenciarme.`", time=3)
    try:
        await e.client.edit_permissions(
            chat.id,
            userid,
            until_date=None,
            send_messages=False,
        )
        await eod(
            xx,
            f"`Silenciado con Exito` [{name}](tg://user?id={userid}) `in {chat.title}`",
            time=5,
        )
    except BaseException as m:
        await eod(xx, f"`{str(m)}`")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
