

"""
✅ Comandos by: @Dextrov -

• `{i}ftyping <time/in secs>`
    `Mostrar escritura falsa en el chat actual. `

• `{i}faudio <time/in secs>`
    `Mostrar acción de grabación falsa en el chat actual. `

• `{i}fvideo <time/in secs>`
    `Mostrar acción de video falso en el chat actual. `

• `{i}fgame <time/in secs>`
    `Scómo la acción de juego falso en el chat actual. `
"""

from . import *


@ultroid_cmd(pattern="ftyping ?(.*)")
async def _(e):
    t = e.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await ban_time(e, t)
            except BaseException:
                return await eod(e, "`Formato incorrecto`")
    await eod(e, f"Inicio de escritura falsa para {t} sec.")
    async with e.client.action(e.chat_id, "typing"):
        await asyncio.sleep(t)


@ultroid_cmd(pattern="faudio ?(.*)")
async def _(e):
    t = e.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await ban_time(e, t)
            except BaseException:
                return await eod(e, "`Formato incorrecto`")
    await eod(e, f"Iniciar grabación de audio falsa para {t} sec.")
    async with e.client.action(e.chat_id, "record-audio"):
        await asyncio.sleep(t)


@ultroid_cmd(pattern="fvideo ?(.*)")
async def _(e):
    t = e.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await ban_time(e, t)
            except BaseException:
                return await eod(e, "`Formato incorrecto`")
    await eod(e, f"Inicio de grabación de video falso para {t} sec.")
    async with e.client.action(e.chat_id, "record-video"):
        await asyncio.sleep(t)


@ultroid_cmd(pattern="fgame ?(.*)")
async def _(e):
    t = e.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await ban_time(e, t)
            except BaseException:
                return await eod(e, "`Formato incorrecto`")
    await eod(e, f"Iniciar juego falso para{t} sec.")
    async with e.client.action(e.chat_id, "game"):
        await asyncio.sleep(t)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
