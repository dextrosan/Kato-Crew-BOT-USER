

"""
✅ Comandos by: @Dextrov -

• `{i}blacklist <word/all words with a space>`
    poner en lista negra la palabra elegida en ese chat.

• `{i}remblacklist <word>`
    Eliminar la palabra de la lista negra..

• `{i}listblacklist`
    enumerar todas las palabras de la lista negra.

  'si una persona usa Word de lista negra, su mensaje será eliminado'
  'Y debes ser administrador en ese chat'
"""


from pyUltroid.functions.blacklist_db import *

from . import *


@ultroid_cmd(pattern="blacklist ?(.*)")
async def af(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí`")
    wrd = e.pattern_match.group(1)
    chat = e.chat_id
    if not (wrd):
        return await eod(e, "`Give the word to blacklist..`")
    wrd = e.text[11:]
    heh = wrd.split(" ")
    for z in heh:
        add_blacklist(int(chat), z.lower())
    await eor(e, f"Done : `{wrd}` Blacklisted here.")


@ultroid_cmd(pattern="remblacklist ?(.*)")
async def rf(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`No eres administrador aquí`")
    wrd = e.pattern_match.group(1)
    chat = e.chat_id
    if not wrd:
        return await eod(e, "`Give the word to remove from blacklist..`")
    wrd = e.text[14:]
    heh = wrd.split(" ")
    for z in heh:
        rem_blacklist(int(chat), z.lower())
    await eor(e, f"Done : `{wrd}` Removed from Blacklist.")


@ultroid_cmd(pattern="listblacklist")
async def lsnote(e):
    if e.is_group:
        if not e._chat.admin_rights:
            return await eod(e, "`You are Not Admin Here`")
    x = list_blacklist(e.chat_id)
    if x:
        sd = "Blacklist Found In This Chats Are\n\n"
        await eor(e, sd + x)
    else:
        await eor(e, "No Blacklist word Found Here")


@ultroid_bot.on(events.NewMessage(incoming=True))
async def bl(e):
    chat = e.chat_id
    x = get_blacklist(int(chat))
    if x and e.text:
        xx = ((e.text).lower()).split()
        yy = x.split("$|")
        for z in xx:
            if z in yy:
                await e.delete()
                break


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
