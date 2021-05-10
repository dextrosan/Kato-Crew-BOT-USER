

"""
✅ Comandos by: @Dextrov -


• `{i}startvc`
    Inicie una llamada de grupo en un grupo.

• `{i}stopvc`
    Detenga la llamada de grupo en un grupo.

• `{i}playvc`
    Inicie Voice Chat Bot para recibir comandos.

• `{i}vcinvite`
    Invite a todos los miembros del grupo en una llamada grupal.
    (Debes estar unido)

• `{i}vcaccess <id/username/reply to msg>`
    Dar acceso al bot de chat de voz.

• `{i}rmvcaccess <id/username/reply to msg>`
    Eliminar el acceso al bot de chat de voz.

• **Comandos del bot de chat de voz**
   `/play ytsearch:song name`
   `/play youtube link`

"""

from pyUltroid.functions.vc_sudos import add_vcsudo, del_vcsudo, get_vcsudos, is_vcsudo
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from . import *


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@ultroid_cmd(
    pattern="stopvc$",
    admins_only=True,
    groups_only=True,
)
async def _(e):
    try:
        await e.client(stopvc(await get_call(e)))
        await eor(e, "`Chat de voz detenido...`")
    except Exception as ex:
        await eor(e, f"`{str(ex)}`")


@ultroid_cmd(
    pattern="playvc$",
)
async def _(e):
    zz = await eor(e, "`VC bot iniciado...`")
    er, out = await bash("npm start")
    LOGS.warning(er)
    LOGS.info(out)
    await zz.edit(f"Failed {er}")


@ultroid_cmd(
    pattern="vcinvite$",
    groups_only=True,
)
async def _(e):
    ok = await eor(e, "`Invitación de miembros al chat de voz...`")
    users = []
    z = 0
    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass
    await ok.edit(f"`Invitar {z} users`")


@ultroid_cmd(
    pattern="startvc$",
    admins_only=True,
    groups_only=True,
)
async def _(e):
    try:
        await e.client(startvc(e.chat_id))
        await eor(e, "`Se inició el chat de voz...`")
    except Exception as ex:
        await eor(e, f"`{str(ex)}`")


@ultroid_cmd(
    pattern="listvcaccess$",
)
async def _(e):
    xx = await eor(e, "`Obtener la lista de usuarios del bot de chat de voz...`")
    mm = get_vcsudos()
    pp = f"**{len(mm)} Usuarios aprobados del bot de chat de voz**\n"
    if len(mm) > 0:
        for m in mm:
            try:
                name = (await e.client.get_entity(int(m))).first_name
                pp += f"• [{name}](tg://user?id={int(m)})\n"
            except ValueError:
                pp += f"• `{int(m)} » No Info`\n"
    await xx.edit(pp)


@ultroid_cmd(
    pattern="rmvcaccess ?(.*)",
)
async def _(e):
    xx = await eor(e, "`Desaprobar el acceso a las funciones del chat de voz...`")
    input = e.pattern_match.group(1)
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        try:
            userid = await get_user_id(input)
            name = (await e.client.get_entity(userid)).first_name
        except ValueError as ex:
            return await eod(xx, f"`{str(ex)}`", time=5)
    else:
        return await eod(xx, "`Responder al mensaje del usuario o agregarlo id/username...`", time=3)
    if not is_vcsudo(userid):
        return await eod(
            xx,
            f"[{name}](tg://user?id={userid})` no está aprobado para usar mi bot de chat de voz.`",
            time=5,
        )
    try:
        del_vcsudo(userid)
        await eod(
            xx,
            f"[{name}](tg://user?id={userid})` se elimina de los usuarios del bot de chat de voz.`",
            time=5,
        )
    except Exception as ex:
        return await eod(xx, f"`{str(ex)}`", time=5)


@ultroid_cmd(
    pattern="vcaccess ?(.*)",
)
async def _(e):
    xx = await eor(e, "`Aprobación para acceder a las funciones de chat de voz...`")
    input = e.pattern_match.group(1)
    if e.reply_to_msg_id:
        userid = (await e.get_reply_message()).sender_id
        name = (await e.client.get_entity(userid)).first_name
    elif input:
        try:
            userid = await get_user_id(input)
            name = (await e.client.get_entity(userid)).first_name
        except ValueError as ex:
            return await eod(xx, f"`{str(ex)}`", time=5)
    else:
        return await eod(xx, "`Responder al mensaje del usuario o agregarlo id/username...`", time=3)
    if is_vcsudo(userid):
        return await eod(
            xx,
            f"[{name}](tg://user?id={userid})` ya está aprobado para usar mi bot de chat de voz.`",
            time=5,
        )
    try:
        add_vcsudo(userid)
        await eod(
            xx,
            f"[{name}](tg://user?id={userid})` Se agrega a las usuarios de Bot de chat de voz.`",
            time=5,
        )
    except Exception as ex:
        return await eod(xx, f"`{str(ex)}`", time=5)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
