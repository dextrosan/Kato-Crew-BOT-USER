

"""
✅ Comandos by: @Dextrov -

• `{i}bash <cmds>`
    Ejecute comandos de Linux en Telegram.

• `{i}eval <cmds>`
    Evalúe los comandos de Python en Telegram.

• `{i}circle`
    Responde a una canción de audio o gif para obtener una nota de video.

• `{i}ls`
    Obtenga todos los archivos dentro de un directorio.

• `{i}bots`
    Muestra el número de bots en el chat actual con su enlace permanente.

• `{i}hl <a link>`
    Incrusta el enlace con un espacio en blanco como mensaje.

• `{i}id`
    Responde una calcomanía para obtener su identificación
    Responder a un usuario para obtener su identificación
    Sin responder, obtendrá la identificación del chat

• `{i}sg <reply to a user><username/id>`
    Obtenga su historial de nombres del usuario que respondió.

• `{i}tr <dest lang code> <(reply to) a message>`
    Obtener mensaje traducido.

• `{i}sysinfo`
    Muestra información del sistema.
"""

import asyncio
import io
import os
import sys
import time
import traceback
from asyncio.exceptions import TimeoutError
from os import remove
from pathlib import Path

import cv2
import emoji
from carbonnow import Carbon
from googletrans import Translator
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantsBots, User
from telethon.utils import pack_bot_file_id

from . import *
from . import humanbytes as hb


@ultroid_cmd(
    pattern="sysinfo$",
)
async def _(e):
    x, y = await bash("neofetch|sed 's/\x1B\\[[0-9;\\?]*[a-zA-Z]//g' >> neo.txt")
    with open("neo.txt", "r") as neo:
        p = (neo.read()).replace("\n\n", "")
    ok = Carbon(code=p)
    haa = await ok.save("neofetch")
    await e.client.send_file(e.chat_id, haa)
    remove("neofetch.jpg")
    remove("neo.txt")


@ultroid_cmd(
    pattern="tr",
)
async def _(event):
    if len(event.text) > 3:
        if not event.text[3] == " ":
            return
    input = event.text[4:6]
    txt = event.text[7:]
    xx = await eor(event, "`Traducir...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input or "en"
    elif input:
        text = txt
        lan = input or "en"
    else:
        return await eod(xx, f"`{hndlr}tr LanguageCode` as reply to a message", time=5)
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        tt = translator.translate(text, dest=lan)
        output_str = f"**TRANSLATED** from {tt.src} to {lan}\n{tt.text}"
        await eor(xx, output_str)
    except Exception as exc:
        await eod(xx, str(exc), time=10)


@ultroid_cmd(
    pattern="id ?(.*)",
)
async def _(event):
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await eor(
                event,
                "**Current Chat ID:**  `{}`\n**From User ID:**  `{}`\n**Bot API File ID:**  `{}`".format(
                    str(event.chat_id),
                    str(r_msg.sender_id),
                    bot_api_file_id,
                ),
            )
        else:
            await eor(
                event,
                "**Chat ID:**  `{}`\n**User ID:**  `{}`".format(
                    str(event.chat_id),
                    str(r_msg.sender_id),
                ),
            )
    elif event.pattern_match.group(1):
        ids = await get_user_id(event.pattern_match.group(1))
        return await eor(
            event,
            "**Chat ID:**  `{}`\n**User ID:**  `{}`".format(
                str(event.chat_id),
                str(ids),
            ),
        )
    else:
        await eor(event, "**Current Chat ID:**  `{}`".format(str(event.chat_id)))


@ultroid_cmd(pattern="bots ?(.*)")
async def _(ult):
    await ult.edit("`...`")
    if ult.is_private:
        user = await ult.get_chat()
        if not user.bot:
            return await ult.edit("`Seariously ?`")

    mentions = "**Bots en este chat**: \n"
    input_str = ult.pattern_match.group(1)
    to_write_chat = await ult.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = f"**Bots en **{input_str}: \n"
        try:
            chat = await ultroid_bot.get_entity(input_str)
        except Exception as e:
            await eor(ult, str(e))
            return None
    try:
        async for x in ultroid_bot.iter_participants(
            chat,
            filter=ChannelParticipantsBots,
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name,
                    x.id,
                    x.id,
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name,
                    x.id,
                    x.id,
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await eor(ult, mentions)


@ultroid_cmd(pattern="hl")
async def _(ult):
    try:
        input = ult.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await eod(ult, "`Ingrese algún enlace`", time=5)
    await eor(ult, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input + ")", link_preview=False)


@ultroid_cmd(
    pattern="circle$",
)
async def _(e):
    a = await e.get_reply_message()
    if a is None:
        return await eor(e, "Responder a un gif o audio")
    if a.document and a.document.mime_type == "audio/mpeg":
        z = await eor(e, "**Cʀᴇᴀᴛɪɴɢ Vɪᴅᴇᴏ Nᴏᴛᴇ**")
        toime = time.time()
        try:
            bbbb = await a.download_media(thumb=-1)
            im = cv2.imread(bbbb)
            dsize = (320, 320)
            output = cv2.resize(im, dsize, interpolation=cv2.INTER_AREA)
            cv2.imwrite("img.png", output)
            thumb = "img.png"
        except TypeError:
            thumb = "./resources/extras/new_thumb.jpg"
        c = await a.download_media(
            "resources/downloads/",
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, z, toime, "Dᴏᴡɴʟᴏᴀᴅɪɴɢ..."),
            ),
        )
        await z.edit("**Dᴏᴡɴʟᴏᴀᴅᴇᴅ...\nNᴏᴡ Cᴏɴᴠᴇʀᴛɪɴɢ...**")
        cmd = [
            "ffmpeg",
            "-i",
            c,
            "-acodec",
            "libmp3lame",
            "-ac",
            "2",
            "-ab",
            "144k",
            "-ar",
            "44100",
            "comp.mp3",
        ]
        proess = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proess.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        mcd = [
            "ffmpeg",
            "-y",
            "-i",
            thumb,
            "-i",
            "comp.mp3",
            "-c:a",
            "copy",
            "circle.mp4",
        ]
        process = await asyncio.create_subprocess_exec(
            *mcd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        taime = time.time()
        await e.client.send_file(
            e.chat_id,
            "circle.mp4",
            thumb=thumb,
            video_note=True,
            reply_to=a,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, z, taime, "Uᴘʟᴏᴀᴅɪɴɢ..."),
            ),
        )
        await z.delete()
        os.system("rm resources/downloads/*")
        os.system("rm circle.mp4 comp.mp3 img.png")
        os.remove(bbbb)
    elif a.document and a.document.mime_type == "video/mp4":
        z = await eor(e, "**Cʀᴇᴀᴛɪɴɢ Vɪᴅᴇᴏ Nᴏᴛᴇ**")
        c = await a.download_media("resources/downloads/")
        await e.client.send_file(
            e.chat_id,
            c,
            video_note=True,
            thumb="resources/extras/new_thumb.jpg",
            reply_to=a,
        )
        await z.delete()
        os.remove(c)
    else:
        return await eor(e, "**Rresponder solo a un archivo gif o de audio**")


@ultroid_cmd(pattern="ls ?(.*)")
async def _(e):
    path = Path(e.pattern_match.group(1))
    if not path:
        path = Path(".")
    else:
        if not os.path.isdir(path):
            return await eod(e, "`Directorio incorrecto.`")
        if not os.listdir(path):
            return await eod(e, "`Este directorio está vacío.`")
    files = path.iterdir()
    pyfiles = []
    jsons = []
    vdos = []
    audios = []
    pics = []
    others = []
    otherfiles = []
    folders = []
    text = []
    apk = []
    exe = []
    zip = []
    book = []
    for file in sorted(files):
        if os.path.isdir(file):
            folders.append("📂 " + str(file))
        elif str(file).endswith(".py"):
            pyfiles.append("🐍 " + str(file))
        elif str(file).endswith(".json"):
            jsons.append("🔮 " + str(file))
        elif str(file).endswith((".mkv", ".mp4", ".avi")):
            vdos.append("🎥 " + str(file))
        elif str(file).endswith((".mp3", ".ogg", ".m4a")):
            audios.append("🔊 " + str(file))
        elif str(file).endswith((".jpg", ".jpeg", ".png", ".webp")):
            pics.append("🖼 " + str(file))
        elif str(file).endswith((".txt", ".text", ".log")):
            text.append("📄 " + str(file))
        elif str(file).endswith((".apk", ".xapk")):
            apk.append("📲 " + str(file))
        elif str(file).endswith(".exe"):
            set.append("⚙ " + str(file))
        elif str(file).endswith((".zip", ".rar")):
            zip.append("🗜 " + str(file))
        elif str(file).endswith((".pdf", ".epub")):
            book.append("📗 " + str(file))
        elif "." in str(file)[1:]:
            others.append("🏷 " + str(file))
        else:
            otherfiles.append("📒 " + str(file))
    omk = [
        *sorted(folders),
        *sorted(pyfiles),
        *sorted(jsons),
        *sorted(zip),
        *sorted(vdos),
        *sorted(pics),
        *sorted(audios),
        *sorted(apk),
        *sorted(exe),
        *sorted(book),
        *sorted(text),
        *sorted(others),
        *sorted(otherfiles),
    ]
    text = ""
    for i in omk:
        emoji = i.split()[0]
        name = i.split(maxsplit=1)[1]
        nam = name.split("/")[-1]
        if os.path.isdir(name):
            size = 0
            for path, dirs, files in os.walk(name):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
            if hb(size):
                text += emoji + f" `{nam}`" + "  `" + hb(size) + "`\n"
            else:
                text += emoji + f" `{nam}`" + "\n"
        else:
            if hb(int(os.path.getsize(name))):
                text += (
                    emoji + f" `{nam}`" + "  `" + hb(int(os.path.getsize(name))) + "`\n"
                )
            else:
                text += emoji + f" `{nam}`" + "\n"

    await eor(e, text)


@ultroid_cmd(
    pattern="bash",
)
async def _(event):
    if not event.out and not is_fullsudo(event.sender_id):
        return await eor(event, "`Este comando está restringido por sudo.`")
    if Redis("I_DEV") != "True":
        await eor(
            event,
            f"Desarrollador restringido!\nSi sabe lo que hace esto y desea continuar\n\n `{HNDLR}setredis I_DEV True`\n\nEsto puede ser peligroso.",
        )
        return
    xx = await eor(event, "`Procesando...`")
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await eod(xx, "`No cmd given`", time=10)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + 100
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    OUT = f"**☞ BASH\n\n• COMANDOD:**\n`{cmd}` \n\n"
    e = stderr.decode()
    if e:
        OUT += f"**• ERROR:** \n`{e}`\n"
    o = stdout.decode()
    if not o:
        o = "Exito"
        OUT += f"**• OUTPUT:**\n`{o}`"
    else:
        _o = o.split("\n")
        o = "\n".join(_o)
        OUT += f"**• OUTPUT:**\n`{o}`"
    if len(OUT) > 4096:
        ultd = OUT.replace("`", "").replace("*", "").replace("_", "")
        with io.BytesIO(str.encode(ultd)) as out_file:
            out_file.name = "bash.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                thumb="resources/extras/new_thumb.jpg",
                allow_cache=False,
                caption=f"`{cmd}`",
                reply_to=reply_to_id,
            )
            await xx.delete()
    else:
        await eor(xx, OUT)


p = print  # ignore: pylint


@ultroid_cmd(
    pattern="eval",
)
async def _(event):
    if len(event.text) > 5:
        if not event.text[5] == " ":
            return
    if not event.out and not is_fullsudo(event.sender_id):
        return await eor(event, "`Este comando está restringido por sudo.`")
    if Redis("I_DEV") != "True":
        await eor(
            event,
            f"Desarrollador restringidod!\nSi sabe lo que hace esto y desea continuar\n\n {HNDLR}setredis I_DEV True\n\nEsto puede ser peligroso.",
        )
        return
    xx = await eor(event, "`Procesando ...`")
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await eod(xx, "`Give some python cmd`", time=5)
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    reply_to_id = event.message.id
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Éxito"
    final_output = (
        "__►__ **EVALPy**\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
            cmd,
            evaluation,
        )
    )
    if len(final_output) > 4096:
        ultd = final_output.replace("`", "").replace("*", "").replace("_", "")
        with io.BytesIO(str.encode(ultd)) as out_file:
            out_file.name = "eval.txt"
            await ultroid_bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                thumb="resources/extras/new_thumb.jpg",
                allow_cache=False,
                caption=f"```{cmd}```",
                reply_to=reply_to_id,
            )
            await xx.delete()
    else:
        await eor(xx, final_output)


async def aexec(code, event):
    e = message = event
    client = event.client
    exec(
        f"async def __aexec(e, client): "
        + "\n message = event = e"
        + "".join(f"\n {l}" for l in code.split("\n")),
    )

    return await locals()["__aexec"](e, e.client)


@ultroid_cmd(
    pattern="sg ?(.*)",
)
async def lastname(steal):
    if BOT_MODE:
        return await eor(steal, "`No puede usar este comando en MODO BOT..`")
    mat = steal.pattern_match.group(1)
    if not (steal.is_reply or mat):
        await eor(steal, "`Utilice este comando con la respuesta o proporcione el username / id...`")
        return
    if mat:
        user_id = await get_user_id(mat)
    message = await steal.get_reply_message()
    if message:
        user_id = message.sender.id
    chat = "@SangMataInfo_bot"
    id = f"/search_id {user_id}"
    check = await ultroid_bot.get_entity(user_id)
    if not isinstance(check, User) or check.bot:
        return await eor(steal, "Responder al mensaje del usuario real !")
    lol = await eor(steal, "`Procesando !...`")
    try:
        async with ultroid_bot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                response = await conv.get_response()
                respond = await conv.get_response()
                responds = await conv.get_response()
            except YouBlockedUserError:
                await lol.edit("Por Favor Desbloquear @sangmatainfo_bot e intenta de nuevo")
                return
            if response.text.startswith("No se encontraron registros"):
                await lol.edit("No se encontraron registros para este usuario.")
                await steal.client.delete_messages(conv.chat_id, [msg.id, response.id])
                return
            else:
                if response.text.startswith("🔗"):
                    await lol.edit(respond.message)
                    await lol.reply(responds.message)
                elif respond.text.startswith("🔗"):
                    await lol.edit(response.message)
                    await lol.reply(responds.message)
                else:
                    await lol.edit(respond.message)
                    await lol.reply(response.message)
            await steal.client.delete_messages(
                conv.chat_id,
                [msg.id, responds.id, respond.id, response.id],
            )
    except TimeoutError:
        return await lol.edit("Error: @SangMataInfo_bot no está respondiendo!.")


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
