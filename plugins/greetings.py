

"""
✅ Comandos by: @Dextrov -

---- Welcomes ----
• `{i}setwelcome <message/reply to message>`
    Establecer mensaje de bienvenida en el chat actual.

• `{i}clearwelcome`
    Elimina la bienvenida en el chat actual.

• `{i}getwelcome`
    Recibe el mensaje de bienvenida en el chat actual.

---- GoodByes ----
• `{i}setgoodbye <message/reply to message>`
    Establecer mensaje de despedida en el chat actual.

• `{i}cleargoodbye`
    Elimina el adiós en el chat actual.

• `{i}getgoodbye`
    Recibe el mensaje de despedida en el chat actual.

"""
import os

from telegraph import upload_file as uf
from telethon.utils import get_display_name, pack_bot_file_id

from . import *

Note = "\n\nNote: `{mention}`, `{group}`, `{count}`, `{name}`, `{fullname}`, `{username}`, `{userid}` can be used as formatting parameters.\n\n"


@ultroid_cmd(pattern="setwelcome")
async def setwel(event):
    x = await eor(event, get_string("com_1"))
    r = await event.get_reply_message()
    if event.is_private:
        return await eod(x, "Utilice esto en un grupo y no en PM!", time=10)
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await bot.download_media(r.media)
            variable = uf(dl)
            os.remove(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eod(x, "`Unsupported Media`")
            else:
                dl = await bot.download_media(r.media)
                variable = uf(dl)
                os.remove(dl)
                m = "https://telegra.ph" + variable[0]
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            add_welcome(event.chat_id, r.message, m)
        else:
            add_welcome(event.chat_id, None, m)
        await eor(x, "`Nota de bienvenida guardada`")
    elif r and r.text:
        add_welcome(event.chat_id, r.message, None)
        await eor(x, "`Nota de bienvenida guardada`")
    else:
        await eod(x, "`Responder al mensaje que desea configurar como bienvenida`")


@ultroid_cmd(pattern="clearwelcome$")
async def clearwel(event):
    if not get_welcome(event.chat_id):
        await eod(event, "`No se estableció la bienvenida!`", time=5)
    delete_welcome(event.chat_id)
    await eod(event, "`Nota de bienvenida eliminada`")


@ultroid_cmd(pattern="getwelcome$")
async def listwel(event):
    wel = get_welcome(event.chat_id)
    if not wel:
        await eod(event, "`¡No se fijó bienvenida!`", time=5)
    msgg = wel["welcome"]
    med = wel["media"]
    await event.reply(f"**Nota de bienvenida en este chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ultroid_bot.on(events.ChatAction())
async def _(event):
    wel = get_welcome(event.chat_id)
    if wel:
        if event.user_joined or event.user_added:
            user = await event.get_user()
            chat = await event.get_chat()
            title = chat.title if chat.title else "este chat"
            pp = await event.client.get_participants(chat)
            count = len(pp)
            mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
            name = user.first_name
            last = user.last_name
            if last:
                fullname = f"{name} {last}"
            else:
                fullname = name
            uu = user.username
            if uu:
                username = f"@{uu}"
            else:
                username = mention
            msgg = wel["welcome"]
            med = wel["media"]
            userid = user.id
            if msgg:
                await event.reply(
                    msgg.format(
                        mention=mention,
                        group=title,
                        count=count,
                        name=name,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                    ),
                    file=med,
                )
            else:
                await event.reply(file=med)


@ultroid_cmd(pattern="setgoodbye")
async def setgb(event):
    x = await eor(event, get_string("com_1"))
    r = await event.get_reply_message()
    if event.is_private:
        return await eod(x, "Utilice esto en un grupo y no en PM!", time=10)
    if r and r.media:
        wut = mediainfo(r.media)
        if wut.startswith(("pic", "gif")):
            dl = await bot.download_media(r.media)
            variable = uf(dl)
            os.remove(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if r.media.document.size > 8 * 1000 * 1000:
                return await eod(x, "`Unsupported Media`")
            else:
                dl = await bot.download_media(r.media)
                variable = uf(dl)
                os.remove(dl)
                m = "https://telegra.ph" + variable[0]
        else:
            m = pack_bot_file_id(r.media)
        if r.text:
            add_goodbye(event.chat_id, r.message, m)
        else:
            add_goodbye(event.chat_id, None, m)
        await eor(x, "`Nota de despedida guardada`")
    elif r and r.text:
        add_goodbye(event.chat_id, r.message, None)
        await eor(x, "`Nota de despedida guardada`")
    else:
        await eod(x, "`Reply to message which u want to set as goodbye`")


@ultroid_cmd(pattern="cleargoodbye$")
async def clearwgb(event):
    if not get_goodbye(event.chat_id):
        await eod(event, "`No se fijó un adiós!`", time=5)
    delete_goodbye(event.chat_id)
    await eod(event, "`Adiós Nota eliminada`")


@ultroid_cmd(pattern="getgoodbye$")
async def listgd(event):
    wel = get_goodbye(event.chat_id)
    if not wel:
        await eod(event, "`No se fijó un adiós!`", time=5)
    msgg = wel["goodbye"]
    med = wel["media"]
    await event.reply(f"**Adiós, Nota en este chat**\n\n`{msgg}`", file=med)
    await event.delete()


@ultroid_bot.on(events.ChatAction())
async def _(event):
    wel = get_goodbye(event.chat_id)
    if wel:
        if event.user_left or event.user_kicked:
            user = await event.get_user()
            chat = await event.get_chat()
            title = chat.title if chat.title else "este chat"
            pp = await event.client.get_participants(chat)
            count = len(pp)
            mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
            name = user.first_name
            last = user.last_name
            if last:
                fullname = f"{name} {last}"
            else:
                fullname = name
            uu = user.username
            if uu:
                username = f"@{uu}"
            else:
                username = mention
            msgg = wel["goodbye"]
            med = wel["media"]
            userid = user.id
            if msgg:
                await event.reply(
                    msgg.format(
                        mention=mention,
                        group=title,
                        count=count,
                        name=name,
                        fullname=fullname,
                        username=username,
                        userid=userid,
                    ),
                    file=med,
                )
            else:
                await event.reply(file=med)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}" + Note})
