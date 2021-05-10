
"""
✅ Comandos by: @Dextrov -

• `{i}delchat`
    Elimina el grupo en el que se usa este comando.

• `{i}getlink`
    Obtener el enlace del grupo en el que se usa este comando.

• `{i}create (b|g|c) <group_name>`
    Crear grupo con un nombre específico.
    b - megagroup/supergroup
    g - small group
    c - channel
"""


from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.tl.functions.channels import CreateChannelRequest, DeleteChannelRequest
from telethon.tl.functions.messages import (
    CreateChatRequest,
    DeleteChatUserRequest,
    ExportChatInviteRequest,
)

from . import *


@ultroid_cmd(
    pattern="delchat$",
    groups_only=True,
)
async def _(e):
    if BOT_MODE:
        return await eor(e, "No puede usar este comando en MODO BOT")
    xx = await eor(e, "`Processing...`")
    try:
        await e.client(DeleteChannelRequest(e.chat_id))
    except TypeError:
        return await eod(xx, "`Cant delete this chat`", time=10)
    except no_admin:
        return await eod(xx, "`I m not an admin`", time=10)
    await e.client.send_message(Var.LOG_CHANNEL, f"#Deleted\nDeleted {e.chat_id}")


@ultroid_cmd(
    pattern="getlink$",
    groups_only=True,
)
async def _(e):
    xx = await eor(e, "`Processing...`")
    try:
        r = await e.client(
            ExportChatInviteRequest(e.chat_id),
        )
    except no_admin:
        return await eod(xx, "`I m not an admin`", time=10)
    await eod(xx, f"Link:- {r.link}")


@ultroid_cmd(
    pattern="create (b|g|c)(?: |$)(.*)",
)
async def _(e):
    if BOT_MODE:
        return await eor(e, "You Cant use this Command in BOT_MODE")
    type_of_group = e.pattern_match.group(1)
    group_name = e.pattern_match.group(2)
    xx = await eor(e, "`Processing...`")
    if type_of_group == "b":
        try:
            r = await e.client(
                CreateChatRequest(
                    users=["@missrose_bot"],
                    title=group_name,
                ),
            )
            created_chat_id = r.chats[0].id
            await e.client(
                DeleteChatUserRequest(
                    chat_id=created_chat_id,
                    user_id="@missrose_bot",
                ),
            )
            result = await e.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                ),
            )
            await xx.edit(
                f"Tu [{group_name}]({result.link}) Jefe de grupo!",
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))
    elif type_of_group == "g" or type_of_group == "c":
        try:
            r = await e.client(
                CreateChannelRequest(
                    title=group_name,
                    about="CREADOR @Dextrov",
                    megagroup=False if type_of_group == "c" else True,
                ),
            )
            created_chat_id = r.chats[0].id
            result = await e.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                ),
            )
            await xx.edit(
                f"Tu [{group_name}]({result.link}) Grupo / Canal Se ha hecho Jefe!",
                link_preview=False,
            )
        except Exception as ex:
            await xx.edit(str(ex))


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
