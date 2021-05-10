

"""
✅ Comandos by: @Dextrov -


🔹 `{i}shift <from channel> | <to channel>`
     Esto transferirá todas las publicaciones antiguas del canal A al canal B.
      (También puedes usar el nombre de usuario o la identificación del canal.)
      example : `{i}shift @abc | @xyz`
      [note - this (" | ") sign is nessesary]

🔹 Para publicar / reenviar automáticamente todos los mensajes nuevos desde cualquier canal de origen a cualquier canal de destino.

   * `asource <channel username or id>`
      Esto agrega el canal de origen a la base de datos
   * `dsource <channel username or id>`
      Esto elimina los canales de origen de la base de datos
   * `listsource <channel username or id>`
      Mostrar lista de canales de origen


   * `{i}adest <channel username or id>`
      Esto agrega sus canales a la base de datos
   * `{i}ddest <channel username or id>`
      Esto elimina sus canales de la base de datos
   * `{i}listdest <channel username or id>`
      Mostrar lista de sus canales

   'puede configurar muchos canales en la base de datos'
   'For activating auto-post use `{i}setredis AUTOPOST True` '
"""

import asyncio

from pyUltroid.functions.ch_db import *

from . import *


@ultroid_bot.on(events.NewMessage())
async def _(e):
    if not udB.get("AUTOPOST") == "True":
        return
    x = get_source_channels()
    th = await e.get_chat()
    for xs in x:
        if str(th.id) not in str(xs):
            return
    y = get_destinations()
    for ys in y:
        try:
            if e.text and not e.media:
                await ultroid_bot.send_message(int(ys), e.text)
            elif e.media and e.text:
                await ultroid_bot.send_file(int(ys), e.media, caption=e.text)
            else:
                await ultroid_bot.send_file(int(ys), e.media)
        except Exception as e:
            await ultroid_bot.send_message(bot.me.id, str(e))


@ultroid_cmd(pattern="shift (.*)")
async def _(e):
    x = e.pattern_match.group(1)
    z = await eor(e, "`processing..`")
    a, b = x.split("|")
    try:
        c = int(a)
    except Exception:
        try:
            c = (await ultroid_bot.get_entity(a)).id
        except Exception:
            await z.edit("canal no válido proporcionado")
            return
    try:
        d = int(b)
    except Exception:
        try:
            d = (await ultroid_bot.get_entity(b)).id
        except Exception:
            await z.edit("canal no válido proporcionado")
            return
    async for msg in ultroid_bot.iter_messages(int(c), reverse=True):
        try:
            await asyncio.sleep(1)
            await ultroid_bot.send_message(int(d), msg)
        except BaseException:
            pass
    await z.edit("Done")


@ultroid_cmd(pattern="asource (.*)")
async def source(e):
    x = e.pattern_match.group(1)
    try:
        y = int(x)
    except Exception:
        try:
            y = int((await bot.get_entity(x)).id)
        except Exception as es:
            print(es)
            return
    if not is_source_channel_added(y):
        add_source_channel(y)
        await eor(e, "Fuente agregada con éxito")
    elif is_source_channel_added(y):
        await eor(e, "El canal de origen ya se agregó")


@ultroid_cmd(pattern="dsource ?(.*)")
async def dd(event):
    chat_id = event.pattern_match.group(1)
    x = await eor(event, "processing")
    if chat_id == "all":
        await x.edit("`Removing...`")
        udB.delete("CH_SOURCE")
        await x.edit("Base de datos de origen borrada.")
        return
    try:
        y = int(chat_id)
    except Exception:
        try:
            y = int((await bot.get_entity(chat_id)).id)
        except Exception as es:
            print(es)
            return
    if is_source_channel_added(y):
        rem_source_channel(y)
        await x.edit("Fuente eliminada de la base de datos")
        await asyncio.sleep(3)
        await x.delete()
    elif is_source_channel_added(y):
        rem_source_channel(y)
        await x.edit("Fuente eliminada de la base de datos")
        await asyncio.sleep(3)
        await x.delete()
    elif not is_source_channel_added(y):
        await x.edit("El canal de origen ya se eliminó de la base de datos. ")
        await asyncio.sleep(3)
        await x.delete()


@ultroid_cmd(pattern="listsource")
async def list_all(event):
    x = await eor(event, "`Calculando...`")
    channels = get_source_channels()
    num = get_no_source_channels()
    if num == 0:
        return await eod(x, "No se agregaron chats.", time=5)
    msg = "Canales de origen en la base de datos:\n"
    for channel in channels:
        name = ""
        try:
            name = (await ultroid.get_entity(int(channel))).title
        except BaseException:
            name = ""
        msg += f"=> **{name}** [`{channel}`]\n"
    msg += f"\nTotal {get_no_source_channels()} canales."
    if len(msg) > 4096:
        MSG = msg.replace("*", "").replace("`", "")
        with io.BytesIO(str.encode(MSG)) as out_file:
            out_file.name = "channels.txt"
            await ultroid_bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Canales en la base de datos",
                reply_to=event,
            )
            await x.delete()
    else:
        await x.edit(msg)


@ultroid_cmd(pattern="adest (.*)")
async def destination(e):
    x = e.pattern_match.group(1)
    try:
        y = int(x)
    except Exception:
        try:
            y = int((await bot.get_entity(x)).id)
        except Exception as es:
            print(es)
            return
    if not is_destination_added(y):
        add_destination(y)
        await eor(e, "Destino agregado exitosamente")
    elif is_destination_added(y):
        await eor(e, "Canal de destino ya agregado")


@ultroid_cmd(pattern="ddest ?(.*)")
async def dd(event):
    chat_id = event.pattern_match.group(1)
    x = await eor(event, "processing")
    if chat_id == "all":
        await x.edit("`Removing...`")
        udB.delete("CH_DESTINATION")
        await x.edit("Se borró la base de datos de destinos.")
        return
    try:
        y = int(chat_id)
    except Exception:
        try:
            y = int((await bot.get_entity(chat_id)).id)
        except Exception as es:
            print(es)
            return
    if is_destination_added(y):
        rem_destination(y)
        await x.edit("Destino eliminado de la base de datos")
        await asyncio.sleep(3)
        await x.delete()
    elif is_destination_added(y):
        rem_destination(y)
        await x.edit("Destino eliminado de la base de datos")
        await asyncio.sleep(3)
        await x.delete()
    elif not is_destination_added(y):
        await x.edit("El canal de destino ya se eliminó de la base de datos. ")
        await asyncio.sleep(3)
        await x.delete()


@ultroid_cmd(pattern="listdest")
async def list_all(event):
    x = await eor(event, "`Calculating...`")
    channels = get_destinations()
    num = get_no_destinations()
    if num == 0:
        return await eod(x, "No se agregaron chats.", time=5)
    msg = "Canales de destino en la base de datos:\n"
    for channel in channels:
        name = ""
        try:
            name = (await ultroid.get_entity(int(channel))).title
        except BaseException:
            name = ""
        msg += f"=> **{name}** [`{channel}`]\n"
    msg += f"\nTotal {get_no_destinations()} canales."
    if len(msg) > 4096:
        MSG = msg.replace("*", "").replace("`", "")
        with io.BytesIO(str.encode(MSG)) as out_file:
            out_file.name = "channels.txt"
            await ultroid_bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Canales de destino en la base de datos",
                reply_to=event,
            )
            await x.delete()
    else:
        await x.edit(msg)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
