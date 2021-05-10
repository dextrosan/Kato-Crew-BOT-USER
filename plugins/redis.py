
"""
✅ Comandos by: @Dextrov -

**Comandos de base de datos, no los utilice si no sabe qué es.**

• `{i}setredis key | value`
    Valor establecido de Redis.
    e.g :
    `{i}setredis hi there`
    `{i}setredis hi there |AL CAPONE BOT here`

• `{i}delredis key`
    Eliminar clave de Redis DB

• `{i}renredis old keyname | new keyname`
    Actualizar nombre de clave
"""

import re

from . import *


@ultroid_cmd(
    pattern="setredis ?(.*)",
)
async def _(ult):
    if not ult.out:
        if not is_fullsudo(ult.sender_id):
            return await eod(ult, "`Este comando está restringido por sudo.`")
    ok = await eor(ult, "`...`")
    try:
        delim = " " if re.search("[|]", ult.pattern_match.group(1)) is None else " | "
        data = ult.pattern_match.group(1).split(delim, maxsplit=1)
        udB.set(data[0], data[1])
        redisdata = Redis(data[0])
        await ok.edit(
            "Redis Key Value Pair Updated\nKey : `{}`\nValue : `{}`".format(
                data[0],
                redisdata,
            ),
        )
    except BaseException:
        await ok.edit("`Algo salió mal`")


@ultroid_cmd(
    pattern="delredis ?(.*)",
)
async def _(ult):
    if not ult.out:
        if not is_fullsudo(ult.sender_id):
            return await eod(ult, "`Este comando está restringido por sudo.`")
    ok = await eor(ult, "`Eliminar datos de Redis ...`")
    try:
        key = ult.pattern_match.group(1)
        udB.delete(key)
        await ok.edit(f"`Clave eliminada correctamente {key}`")
    except BaseException:
        await ok.edit("`Algo salió mal`")


@ultroid_cmd(
    pattern="renredis ?(.*)",
)
async def _(ult):
    if not ult.out:
        if not is_fullsudo(ult.sender_id):
            return await eod(ult, "`Este comando está restringido por sudo.`")
    ok = await eor(ult, "`...`")
    delim = " " if re.search("[|]", ult.pattern_match.group(1)) is None else " | "
    data = ult.pattern_match.group(1).split(delim)
    if Redis(data[0]):
        try:
            udB.rename(data[0], data[1])
            await ok.edit(
                "Redis Key Rename Successful\nOld Key : `{}`\nNew Key : `{}`".format(
                    data[0],
                    data[1],
                ),
            )
        except BaseException:
            await ok.edit("Algo salió mal ...")
    else:
        await ok.edit("Clave no encontrada")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
