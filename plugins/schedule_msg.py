
"""
✅ Comandos by: @Dextrov -

•`{i}schedule <text/reply to msg> <time>`
    Con el tiempo, puede usar el segundo como número, o como 1h o 1m
    eg. `{i}horario Hola 100` Entrega el mensaje después de 100 seg.
    eg. `{i}horario Hola 1h` Entrega el mensaje después de una hora.
"""

from datetime import timedelta

from . import *


@ultroid_cmd(pattern="schedule ?(.*)")
async def _(e):
    x = e.pattern_match.group(1)
    xx = await e.get_reply_message()
    if x and not xx:
        y = x.split(" ")[-1]
        k = x.replace(y, "")
        if y.isdigit():
            await ultroid_bot.send_message(
                e.chat_id, k, schedule=timedelta(seconds=int(y))
            )
            await eod(e, "`Mensaje programado correctamente`")
        else:
            try:
                z = await ban_time(e, y)
                await ultroid_bot.send_message(e.chat_id, k, schedule=z)
                await eod(e, "`Mensaje programado correctamente`")
            except BaseException:
                await eod(e, "`Formato incorrecto`")
    elif xx and x:
        if x.isdigit():
            await e.client.send_message(
                e.chat_id, xx, schedule=timedelta(seconds=int(x))
            )
            await eod(e, "`Mensaje programado correctamente`")
        else:
            try:
                z = await ban_time(e, x)
                await ultroid_bot.send_message(e.chat_id, xx, schedule=z)
                await eod(e, "`Mensaje programado correctamente`")
            except BaseException:Frmato incorrecto`")
    else:
        return await eod(e, "`Formato incorrecto `")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
