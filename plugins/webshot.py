

"""
✅ Comandos by: @Dextrov -

• `{i}webshot <url>`
    Obtenga una captura de pantalla de la página web.

"""

import requests

from . import *


@ultroid_cmd(pattern="webshot")
async def webss(event):
    xx = await eor(event, get_string("com_1"))
    mssg = event.text.split(" ", maxsplit=2)
    try:
        xurl = mssg[1]
    except IndexError:
        return await eod(xx, "`Ponga una URL por favor!`", time=5)
    try:
        requests.get(xurl)
    except requests.ConnectionError:
        return await eod(xx, "Invalid URL!", time=5)
    except requests.exceptions.MissingSchema:
        try:
            r = requests.get("https://" + xurl)
        except requests.ConnectionError:
            try:
                r2 = requests.get("http://" + xurl)
            except requests.ConnectionError:
                return await eod(xx, "URL Invalida!", time=5)

    lnk = f"https://shot.screenshotapi.net/screenshot?url={xurl}"
    ok = requests.get(lnk).json()
    try:
        sshot = ok["screenshot"]
    except BaseException:
        return await eod(xx, "Algo salió mal :(", time=10)
    await xx.reply(
        f"**WebShot Generada**\n**URL**: {xurl}",
        file=sshot,
        link_preview=False,
        force_document=True,
    )
    await xx.delete()


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
