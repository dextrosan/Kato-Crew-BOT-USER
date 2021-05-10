

"""
✅ Comandos by: @Dextrov -

• {i}unsplash <search query> ; <no of pics>
    Búsqueda de imágenes de Unsplash.

"""


import urllib

import requests as r
from bs4 import BeautifulSoup as bs

from . import *


@ultroid_cmd(pattern="unsplash ?(.*)")
async def searchunsl(ult):
    match = ult.pattern_match.group(1)
    if not match:
        return await eor(ult, "Dame algo para buscar")
    if ";" in match:
        num = int(match.split(";")[1])
        query = match.split(";")[0]
    else:
        num = 5
        query = match
    tep = await eor(ult, "`Procesando... `")
    res = autopicsearch(query)
    if len(res) == 0:
        return await eod(ult, "No se han encontrado resultados !")
    qas = res[:num]
    dir = "resources/downloads"
    CL = []
    nl = 0
    for rp in qas:
        li = "https://unsplash.com" + rp["href"]
        ct = r.get(li).content
        bst = bs(ct, "html.parser", from_encoding="utf-8")
        ft = bst.find_all("img", "_2UpQX")[0]["src"]
        Hp = dir + "img" + f"{nl}.png"
        urllib.request.urlretrieve(ft, Hp)
        CL.append(Hp)
        nl += 1
    await bot.send_file(
        ult.chat_id, CL, caption=f"Subido {len(qas)} Images\n", album=True
    )
    await tep.delete()


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
