

"""
✅ Comandos by: @Dextrov -

• `{i}meaning <word>`
    Entiende el significado de la palabra.

• `{i}synonym <word>`
    Obtén todos los sinónimos.

• `{i}antonym <word>`
    Obtén todos los antónimos.

• `{i}ud <word>`
    Obtener la definición de la palabra del diccionario urbano.
"""

import asyncurban
from PyDictionary import PyDictionary

from . import *

dictionary = PyDictionary()


@ultroid_cmd(
    pattern="meaning",
)
async def mean(event):
    evid = event.message.id
    xx = await eor(event, get_string("com_1"))
    wrd = event.text.split(" ", maxsplit=1)[1]
    ok = dictionary.meaning(wrd)
    try:
        p = ok["Noun"]
    except BaseException:
        return await xx.edit("Oops! ¡No se encontró tal palabra!")
    x = get_string("wrd_1").format(wrd)
    c = 1
    for i in p:
        x += f"**{c}.** `{i}`\n"
        c += 1
    if len(x) > 4096:
        with io.BytesIO(str.encode(x)) as fle:
            fle.name = f"{wrd}-meanings.txt"
            await ultroid_bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=f"Meanings of {wrd}",
                reply_to=evid,
            )
            await xx.delete()
    else:
        await xx.edit(x)


@ultroid_cmd(
    pattern="synonym",
)
async def mean(event):
    evid = event.message.id
    xx = await eor(event, get_string("com_1"))
    wrd = event.text.split(" ", maxsplit=1)[1]
    ok = dictionary.synonym(wrd)
    x = get_string("wrd_2").format(wrd)
    c = 1
    try:
        for i in ok:
            x += f"**{c}.** `{i}`\n"
            c += 1
        if len(x) > 4096:
            with io.BytesIO(str.encode(x)) as fle:
                fle.name = f"{wrd}-synonyms.txt"
                await ultroid_bot.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=f"Synonyms of {wrd}",
                    reply_to=evid,
                )
                await xx.delete()
        else:
            await xx.edit(x)
    except Exception as e:
        await xx.edit(f"Sin sinónimo encontrado !!\n{str(e)}")


@ultroid_cmd(
    pattern="antonym",
)
async def mean(event):
    evid = event.message.id
    xx = await eor(event, get_string("com_1"))
    wrd = event.text.split(" ", maxsplit=1)[1]
    ok = dictionary.antonym(wrd)
    x = get_string("wrd_3").format(wrd)
    c = 1
    try:
        for i in ok:
            x += f"**{c}.** `{i}`\n"
            c += 1
        if len(x) > 4096:
            with io.BytesIO(str.encode(x)) as fle:
                fle.name = f"{wrd}-antonyms.txt"
                await ultroid_bot.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=f"Antonyms of {wrd}",
                    reply_to=evid,
                )
                await xx.delete()
        else:
            await xx.edit(x)
    except Exception as e:
        await xx.edit(f"¡No se ha encontrado ningún antónimo!\n{str(e)}")


@ultroid_cmd(pattern="ud (.*)")
async def _(event):
    xx = await eor(event, get_string("com_1"))
    word = event.pattern_match.group(1)
    if word is None:
        return await xx.edit("`No word given!`")
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await xx.edit(
            f"**Texto**: `{mean.word}`\n\n**Significado**: `{mean.definition}`\n\n**Ejemplo**: __{mean.example}__",
        )
    except asyncurban.WordNotFoundError:
        await xx.edit(f"**No se encontraron resultados para** `{word}`")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
