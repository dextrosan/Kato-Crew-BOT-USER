

"""
✅ Comandos by: @Dextrov -

•`{i}addclean`
    Limpiar todos los mensajes de acción próximos en el chat agregado como si alguien se uniera / dejó / pin, etc..

•`{i}remclean`
    Elimina el chat de la base de datos.

•`{i}listclean`
   Para obtener una lista de todos los chats donde está activado.

"""

from pyUltroid.functions.clean_db import *

from . import *


@ultroid_cmd(pattern="addclean$", admins_only=True)
async def _(e):
    add_clean(e.chat_id)
    await eod(e, "Configuración de acción limpia agregada para este chat ")
    async for x in ultroid_bot.iter_messages(e.chat_id, limit=3000):
        if x.action:
            await x.delete()


@ultroid_cmd(pattern="remclean$")
async def _(e):
    rem_clean(e.chat_id)
    await eod(e, "Se eliminó la configuración de acción limpia para este chat")


@ultroid_cmd(pattern="listclean$")
async def _(e):
    k = udB.get("CLEANCHAT")
    if k:
        k = k.split(" ")
        o = ""
        for x in k:
            try:
                title = (await ultroid_bot.get_entity(int(x))).title
            except BaseException:
                title = "`ID Invalida`"
            o += x + " " + title + "\n"
        await eor(e, o)
    else:
        await eod(e, "`No Chat Added`")


@ultroid_bot.on(events.ChatAction())
async def _(event):
    if is_clean_added(event.chat_id):
        try:
            await event.delete()
        except BaseException:
            pass


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
