
"""
✅ Comandos by: @Dextrov -

• `{i}save <reply message>`
    Save that replied msg to ur saved messages box.

"""
from . import *


@ultroid_cmd(pattern="save$")
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e, "Responder a cualquier mensaje para guardarlo en sus mensajes guardados", time=5
        )
    await ultroid_bot.send_message(e.sender_id, x)
    await eod(e, "Mensaje guardado en su Pm / Mensajes guardados.", time=5)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
