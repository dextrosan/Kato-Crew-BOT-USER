
"""
✅ Comandos by: @Dextrov -

• `{i}addnote <word><reply to a message>`
    agregue una nota en el chat usado con el mensaje respondido y la palabra elegida.

• `{i}remnote <word>`
    Elimina la nota del chat usado.

• `{i}listnote`
    enumerar todas las notas.

• Use :
   establecer notas en grupo para que todos puedan usarlo.
   type `#(Keyword of note)` to get it
"""
import os

from pyUltroid.functions.notes_db import *
from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id

from . import *


@ultroid_cmd(pattern="addnote ?(.*)")
async def an(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí.", time=5)
    wrd = (e.pattern_match.group(1)).lower()
    wt = await e.get_reply_message()
    chat = e.chat_id
    if not (wt and wrd):
        return await eod(e, "`Use este comando con respuesta y palabra para usar una nota.`")
    if "#" in wrd:
        wrd = wrd.replace("#", "")
    if wt and wt.media:
        wut = mediainfo(wt.media)
        if wut.startswith(("pic", "gif")):
            dl = await bot.download_media(wt.media)
            variable = uf(dl)
            os.remove(dl)
            m = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if wt.media.document.size > 8 * 1000 * 1000:
                return await eod(x, "`Unsupported Media`")
            else:
                dl = await bot.download_media(wt.media)
                variable = uf(dl)
                os.remove(dl)
                m = "https://telegra.ph" + variable[0]
        else:
            m = pack_bot_file_id(wt.media)
        if wt.text:
            add_note(int(chat), wrd, wt.text, m)
        else:
            add_note(int(chat), wrd, None, m)
    else:
        add_note(int(chat), wrd, wt.text, None)
    await eor(e, f"Done Note : `#{wrd}` saved.")


@ultroid_cmd(pattern="remnote ?(.*)")
async def rn(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí.", time=5)
    wrd = (e.pattern_match.group(1)).lower()
    chat = e.chat_id
    if not wrd:
        return await eod(e, "`Dame el manejador de notas que quieres eliminar.`")
    if wrd.startswith("#"):
        wrd = wrd.replace("#", "")
    rem_note(int(chat), wrd)
    await eor(e, f"Hecho, Nota: `#{wrd}` Removida.")


@ultroid_cmd(pattern="listnote$")
async def lsnote(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí.", time=5)
    x = list_note(e.chat_id)
    if x:
        sd = "Las notas encontradas en estos chats son\n\n"
        await eor(e, sd + x)
    else:
        await eor(e, "No se encontraron notas aquí")


@ultroid_bot.on(events.NewMessage())
async def notes(e):
    xx = e.text
    if not xx.startswith("#"):
        return
    xx = (xx.replace("#", "")).lower()
    chat = e.chat_id
    x = get_notes(int(chat))
    if x:
        if " " in xx:
            xx = xx.split(" ")[0]
        k = get_reply(chat, xx)
        if k:
            msg = k["msg"]
            media = k["media"]
            await e.reply(msg, file=media)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
