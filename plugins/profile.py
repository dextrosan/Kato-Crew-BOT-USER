

"""
✅ Comandos by: @Dextrov -

• `{i}setname <first name // last name>`
    Cambia tu nombre de perfil.

• `{i}setbio <bio>`
    Cambia tu biografía de perfil.

• `{i}setpic <reply to pic>`
    Cambia tu foto de perfil.

• `{i}delpfp <n>(optional)`
    Elimine una foto de perfil, si no se proporciona ningún valor, de lo contrario elimine una cantidad  de fotos.

• `{i}poto <username>`
    Sube la foto de Chat/User si está disponible.
"""

import asyncio
import os

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import (
    DeletePhotosRequest,
    GetUserPhotosRequest,
    UploadProfilePhotoRequest,
)
from telethon.tl.types import InputPhoto

from . import *

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

# bio changer


@ultroid_cmd(
    pattern="setbio ?(.*)",
)
async def _(ult):
    ok = await eor(ult, "...")
    set = ult.pattern_match.group(1)
    try:
        await ultroid_bot(UpdateProfileRequest(about=set))
        await ok.edit(f"La biografía del perfil cambió a\n`{set}`")
    except Exception as ex:
        await ok.edit("Se produjo un error.\n`{}`".format(str(ex)))
    await asyncio.sleep(10)
    await ok.delete()


# name changer


@ultroid_cmd(
    pattern="setname ?((.|//)*)",
)
async def _(ult):
    ok = await eor(ult, "...")
    names = ult.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "//" in names:
        first_name, last_name = names.split("//", 1)
    try:
        await ultroid_bot(
            UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
            ),
        )
        await ok.edit(f"Nombre cambiado a `{names}`")
    except Exception as ex:
        await ok.edit("Se produjo un error.\n`{}`".format(str(ex)))
    await asyncio.sleep(10)
    await ok.delete()


# profile pic


@ultroid_cmd(
    pattern="setpic$",
)
async def _(ult):
    ok = await eor(ult, "...")
    reply_message = await ult.get_reply_message()
    await ok.edit("`Descargando esa foto...`")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await ultroid_bot.download_media(reply_message, TMP_DOWNLOAD_DIRECTORY)
    except Exception as ex:
        await ok.edit("Se produjo un error.\n`{}`".format(str(ex)))
    else:
        if photo:
            await ok.edit("`Subiéndolo a mi perfil...`")
            file = await ultroid_bot.upload_file(photo)
            try:
                await ultroid_bot(UploadProfilePhotoRequest(file))
            except Exception as ex:
                await ok.edit("Se produjo un error.\n`{}`".format(str(ex)))
            else:
                await ok.edit("`Mi foto de perfil ha sido cambiada !`")
    await asyncio.sleep(10)
    await ok.delete()
    try:
        os.remove(photo)
    except Exception as ex:
        LOGS.exception(ex)


# delete profile pic(s)


@ultroid_cmd(
    pattern="delpfp ?(.*)",
)
async def remove_profilepic(delpfp):
    ok = await eor(delpfp, "...")
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await ultroid_bot(
        GetUserPhotosRequest(user_id=delpfp.from_id, offset=0, max_id=0, limit=lim),
    )
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(
                id=sep.id,
                access_hash=sep.access_hash,
                file_reference=sep.file_reference,
            ),
        )
    await ultroid_bot(DeletePhotosRequest(id=input_photos))
    await ok.edit(f"`Eliminado con éxito {len(input_photos)} foto de perfil(s).`")
    await asyncio.sleep(10)
    await ok.delete()


@ultroid_cmd(pattern="poto ?(.*)")
async def gpoto(e):
    ult = e.pattern_match.group(1)
    a = await eor(e, "`Procesando...`")
    if not ult and e.is_reply:
        gs = await e.get_reply_message()
        ult = gs.sender_id
    try:
        okla = await ultroid_bot.download_profile_photo(
            ult,
            "profile.jpg",
            download_big=True,
        )
        await a.delete()
        await ultroid_bot.send_message(e.chat_id, file=okla)
        os.remove(okla)
    except Exception as er:
        await eor(e, f"ERROR - {str(er)}")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
