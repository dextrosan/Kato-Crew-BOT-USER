

"""
✅ Comandos by: @Dextrov -

• `{i}install <reply to plugin>`
    Para instalar elplugin,
   `{i}install f`
    Para forzar la instalación.

• `{i}uninstall <plugin name>`
    Para descargar y retirar el plugin.

• `{i}load <plugin name>`
    Para cargar no oficial descargado plugin.

• `{i}unload <plugin name>`
    Para descargar no oficial plugin.

• `{i}help <plugin name>`
    Te muestra un menú de ayuda (como esto) para cada plugin.
"""

import os

from telethon import Button

from . import *


@in_pattern(
    "send ?(.*)",
)
@in_owner
async def inline_handler(event):
    builder = event.builder
    input_str = event.pattern_match.group(1)
    if input_str is None or input_str == "":
        plugs = await event.builder.article(
            title=f"Cual plugin?",
            text="Sin módulo",
            buttons=[
                Button.switch_inline(
                    "Busca de nuevo..?",
                    query="Enviar ",
                    same_peer=True,
                ),
            ],
        )
        await event.answer(plugs)
    else:
        try:
            ultroid = builder.document(
                f"plugins/{input_str}.py",
                title=f"{input_str}.py",
                description=f"Module {input_str} Found",
                text=f"{input_str}.py use el botón de abajo para pegar en neko y raw..",
                buttons=[
                    [
                        Button.switch_inline(
                            "Busca de nuevo..?",
                            query="Enviar ",
                            same_peer=True,
                        ),
                    ],
                    [
                        Button.inline(
                            "Paste?",
                            data=f"pasta-plugins/{input_str}.py",
                        ),
                    ],
                ],
            )
            await event.answer([DEXTRO])
            return
        except BaseException:
            ultroidcode = builder.article(
                title=f"Modulo {input_str}.py No encontrado",
                description=f"No existe tal módulo",
                text=f"Ningún módulo nombrado {input_str}.py",
                buttons=[
                    [
                        Button.switch_inline(
                            "Buscar de nuevo",
                            query="Enviar ",
                            same_peer=True,
                        ),
                    ],
                ],
            )
            await event.answer([ultroidcode])
            return


@ultroid_cmd(
    pattern="install",
)
async def install(event):
    if not is_fullsudo(event.sender_id):
        return await eod(event, "`Este comando está restringido por sudo.`")
    await safeinstall(event)


@ultroid_cmd(
    pattern=r"unload ?(.*)",
)
async def unload(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Give name of plugin which u want to unload`")
        return
    lsd = os.listdir("addons")
    lst = os.listdir("plugins")
    zym = shortname + ".py"
    if zym in lsd:
        try:
            un_plug(shortname)
            await eod(event, f"**Uɴʟᴏᴀᴅᴇᴅ** `{shortname}` **Sᴜᴄᴄᴇssғᴜʟʟʏ.**", time=3)
        except Exception as ex:
            return await eor(event, str(ex))
    elif zym in lst:
        return await eod(event, "**no puedes descargar plugins oficiales**", time=3)
    else:
        return await eod(event, f"**Nᴏ Pʟᴜɢɪɴ Nᴀᴍᴇᴅ** `{shortname}`", time=3)


@ultroid_cmd(
    pattern=r"uninstall ?(.*)",
)
async def uninstall(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Give name of plugin which u want to uninstall`")
        return
    lsd = os.listdir("addons")
    lst = os.listdir("plugins")
    zym = shortname + ".py"
    if zym in lsd:
        try:
            un_plug(shortname)
            await eod(event, f"**Uɴɪɴsᴛᴀʟʟᴇᴅ** `{shortname}` **Sᴜᴄᴄᴇssғᴜʟʟʏ.**", time=3)
            os.remove(f"addons/{shortname}.py")
        except Exception as ex:
            return await eor(event, str(ex))
    elif zym in lst:
        return await eod(event, "**no puedes descargar plugins oficiales**", time=3)
    else:
        return await eod(event, f"**Nᴏ Pʟᴜɢɪɴ Nᴀᴍᴇᴅ** `{shortname}`", time=3)


@ultroid_cmd(
    pattern=r"load ?(.*)",
)
async def load(event):
    shortname = event.pattern_match.group(1)
    if not shortname:
        await eor(event, "`Give name of plugin which u want to load`")
        return
    try:
        try:
            un_plug(shortname)
        except BaseException:
            pass
        load_addons(shortname)
        await eod(event, f"**Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴏᴀᴅᴇᴅ** `{shortname}`", time=3)
    except Exception as e:
        await eod(
            event,
            f"**No puede cargar** `{shortname}` **debido al siguiente error.**\n`{str(e)}`",
            time=3,
        )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
