

"""
✅ Comandos by: @Dextrov -

• `{i}a` or `{i}approve`
    Aprobar a alguien en PM.

• `{i}da` or `{i}disapprove`
    Desaprobar a alguien en PM.

• `{i}block`
    Para bloquear a alguien en PM.

• `{i}unblock`
    Para desbloquear a alguien en PM.

• `{i}nologpm`
    Para detener el registro de ese usuario.

• `{i}logpm`
    Comienza a registrar de nuevo desde ese usuario.
"""

import re

from pyUltroid.functions.logusers_db import *
from pyUltroid.functions.pmpermit_db import *
from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.utils import get_display_name

from . import *

# ========================= CONSTANTS =============================
COUNT_PM = {}
LASTMSG = {}
if Redis("PMPIC"):
    PMPIC = Redis("PMPIC")
else:
    PMPIC = "https://telegra.ph/e3-05-10"

UND = get_string("pmperm_1")

if not Redis("PM_TEXT"):
    UNAPPROVED_MSG = """
**PM Seguridad de {ON}!**

{UND}

Tu tienes {warn}/{twarn} advertencias!"""
else:
    UNAPPROVED_MSG = (
        """
**PM Seguridad de {ON}!**"""
        f"""

{Redis("PM_TEXT")}
"""
        """

{UND}

Tu tienes {warn}/{twarn} advertencias!"""
    )

UNS = get_string("pmperm_2")
# 1
if Redis("PMWARNS"):
    try:
        WARNS = int(Redis("PMWARNS"))
    except BaseException:
        WARNS = 4
else:
    WARNS = 4
NO_REPLY = get_string("pmperm_3")
PMCMDS = [
    f"{hndlr}a",
    f"{hndlr}approve",
    f"{hndlr}da",
    f"{hndlr}disapprove",
    f"{hndlr}block",
    f"{hndlr}unblock",
]
# =================================================================


@ultroid_cmd(
    pattern="logpm$",
)
async def _(e):
    if not e.is_private:
        return await eod(e, "`Úsame en privado.`", time=3)
    if is_logger(str(e.chat_id)):
        nolog_user(str(e.chat_id))
        return await eod(e, "`Ahora registraré mensajes desde aquí.`", time=3)
    else:
        return await eod(e, "`Wasm registrando mensajes desde aquí.`", time=3)


@ultroid_cmd(
    pattern="nologpm$",
)
async def _(e):
    if not e.is_private:
        return await eod(e, "`Úsame en privado.`", time=3)
    if not is_logger(str(e.chat_id)):
        log_user(str(e.chat_id))
        return await eod(e, "`Ahora no registraré mensajes de aquí.`", time=3)
    else:
        return await eod(e, "`No estaba registrando mensajes de aquí.`", time=3)


@ultroid_bot.on(
    events.NewMessage(
        incoming=True,
        func=lambda e: e.is_private,
    ),
)
async def permitpm(event):
    user = await event.get_chat()
    if user.bot or user.is_self or user.verified:
        return
    if is_logger(user.id):
        return
    if Redis("PMLOG") == "True":
        pl = udB.get("PMLOGGROUP")
        if pl is not None:
            return await event.forward_to(int(pl))
        await event.forward_to(Var.LOG_CHANNEL)


sett = Redis("PMSETTING")
if sett is None:
    sett = True
if sett == "True" and sett != "False":

    @ultroid_bot.on(
        events.NewMessage(
            outgoing=True,
            func=lambda e: e.is_private,
        ),
    )
    async def autoappr(e):
        miss = await e.get_chat()
        if miss.bot or miss.is_self or miss.verified or Redis("AUTOAPPROVE") != "True":
            return
        if str(miss.id) in DEVLIST:
            return
        mssg = e.text
        if mssg.startswith(HNDLR):  # do not approve if outgoing is a command.
            return
        if not is_approved(e.chat_id):
            approve_user(e.chat_id)
            async for message in e.client.iter_messages(e.chat_id, search=UND):
                await message.delete()
            async for message in e.client.iter_messages(e.chat_id, search=UNS):
                await message.delete()
            if Var.LOG_CHANNEL:
                name = await e.client.get_entity(e.chat_id)
                name0 = str(name.first_name)
                await e.client.send_message(
                    Var.LOG_CHANNEL,
                    f"#AutoApproved\npor mensaje saliente\nUser - [{name0}](tg://user?id={e.chat_id})",
                )

    @ultroid_bot.on(
        events.NewMessage(
            incoming=True,
            func=lambda e: e.is_private,
        ),
    )
    async def permitpm(event):
        user = await event.get_chat()
        if user.bot or user.is_self or user.verified:
            return
        if str(user.id) in DEVLIST:
            return
        apprv = is_approved(user.id)
        if not apprv and event.text != UND:
            name = user.first_name
            if user.last_name:
                fullname = f"{name} {user.last_name}"
            else:
                fullname = name
            username = f"@{user.username}"
            mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
            count = len(get_approved())
            try:
                wrn = COUNT_PM[user.id] + 1
            except KeyError:
                try:
                    await asst.send_message(
                        Var.LOG_CHANNEL,
                        f"PM entrante de {mention}!",
                        buttons=[
                            Button.inline("Aprobar PM", data=f"approve_{user.id}"),
                            Button.inline("Bloquear PM", data=f"block_{user.id}"),
                        ],
                    )
                except BaseException:
                    await ultroid.send_message(
                        Var.LOG_CHANNEL, f"PM entrante de {mention}!"
                    )
                wrn = 1
            if user.id in LASTMSG:
                prevmsg = LASTMSG[user.id]
                if event.text != prevmsg:
                    if "PMSecurity" in event.text:
                        return
                    async for message in event.client.iter_messages(
                        user.id,
                        search=UND,
                    ):
                        await message.delete()

                    async for message in event.client.iter_messages(
                        user.id,
                        search=UNS,
                    ):
                        await message.delete()
                    await event.client.send_file(
                        user.id,
                        PMPIC,
                        caption=UNAPPROVED_MSG.format(
                            ON=OWNER_NAME,
                            warn=wrn,
                            twarn=WARNS,
                            UND=UND,
                            name=name,
                            fullname=fullname,
                            username=username,
                            count=count,
                            mention=mention,
                        ),
                    )
                elif event.text == prevmsg:
                    async for message in event.client.iter_messages(
                        user.id,
                        search=UND,
                    ):
                        await message.delete()
                    await event.client.send_file(
                        user.id,
                        PMPIC,
                        caption=UNAPPROVED_MSG.format(
                            ON=OWNER_NAME,
                            warn=wrn,
                            twarn=WARNS,
                            UND=UND,
                            name=name,
                            fullname=fullname,
                            username=username,
                            count=count,
                            mention=mention,
                        ),
                    )
                LASTMSG.update({user.id: event.text})
            else:
                async for message in event.client.iter_messages(user.id, search=UND):
                    await message.delete()
                await event.client.send_file(
                    user.id,
                    PMPIC,
                    caption=UNAPPROVED_MSG.format(
                        ON=OWNER_NAME,
                        warn=wrn,
                        twarn=WARNS,
                        UND=UND,
                        name=name,
                        fullname=fullname,
                        username=username,
                        count=count,
                        mention=mention,
                    ),
                )
                LASTMSG.update({user.id: event.text})
            if user.id not in COUNT_PM:
                COUNT_PM.update({user.id: 1})
            else:
                COUNT_PM[user.id] = COUNT_PM[user.id] + 1
            if COUNT_PM[user.id] >= WARNS:
                async for message in event.client.iter_messages(user.id, search=UND):
                    await message.delete()
                await event.respond(UNS)
                try:
                    del COUNT_PM[user.id]
                    del LASTMSG[user.id]
                except KeyError:
                    if Var.LOG_CHANNEL:
                        await event.client.send_message(
                            Var.LOG_CHANNEL,
                            "¡PMPermit está en mal estado! Por favor reinicie el bot!!",
                        )
                        return LOGS.info("COUNT_PM is messed.")
                await event.client(BlockRequest(user.id))
                await event.client(ReportSpamRequest(peer=user.id))
                if Var.LOG_CHANNEL:
                    name = await event.client.get_entity(user.id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        Var.LOG_CHANNEL,
                        f"[{name0}](tg://user?id={user.id}) HAS SIDO BLOQUEADO POR SPAM BY @Dextrov.",
                    )

    @ultroid_cmd(
        pattern="(a|approve)(?: |$)",
    )
    async def approvepm(apprvpm):
        if apprvpm.reply_to_msg_id:
            reply = await apprvpm.get_reply_message()
            replied_user = await apprvpm.client.get_entity(reply.sender_id)
            aname = replied_user.id
            if str(aname) in DEVLIST:
                return await eor(
                    apprvpm,
                    "Lol, él es mi desarrollador\nÉl está auto aprobado",
                )
            name0 = str(replied_user.first_name)
            uid = replied_user.id
            if not is_approved(uid):
                approve_user(uid)
                await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `aprobado para PM!`")
                await asyncio.sleep(3)
                await apprvpm.delete()
            else:
                await apprvpm.edit("`El usuario ya puede ser aprobado.`")
                await asyncio.sleep(5)
                await apprvpm.delete()
        elif apprvpm.is_private:
            user = await apprvpm.get_chat()
            aname = await apprvpm.client.get_entity(user.id)
            if str(user.id) in DEVLIST:
                return await eor(
                    apprvpm,
                    "Lol, él es mi desarrollador\nÉl está auto aprobado",
                )
            name0 = str(aname.first_name)
            uid = user.id
            if not is_approved(uid):
                approve_user(uid)
                await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `aprobado para PM!`")
                async for message in apprvpm.client.iter_messages(user.id, search=UND):
                    await message.delete()
                async for message in apprvpm.client.iter_messages(user.id, search=UNS):
                    await message.delete()
                await asyncio.sleep(3)
                await apprvpm.delete()
                if Var.LOG_CHANNEL:
                    await apprvpm.client.send_message(
                        Var.LOG_CHANNEL,
                        f"#APROVADO\nUser: [{name0}](tg://user?id={uid})",
                    )
            else:
                await apprvpm.edit("`El usuario ya puede ser aprobado.`")
                await asyncio.sleep(5)
                await apprvpm.delete()
                if Var.LOG_CHANNEL:
                    await apprvpm.client.send_message(
                        Var.LOG_CHANNEL,
                        f"#APROVADO\nUser: [{name0}](tg://user?id={uid})",
                    )
        else:
            await apprvpm.edit(NO_REPLY)

    @ultroid_cmd(
        pattern="(da|disapprove)(?: |$)",
    )
    async def disapprovepm(e):
        if e.reply_to_msg_id:
            reply = await e.get_reply_message()
            replied_user = await e.client.get_entity(reply.sender_id)
            aname = replied_user.id
            if str(aname) in DEVLIST:
                return await eor(
                    e,
                    "`Lol, él es mi desarrollador\nNo puede ser desaprobado.`",
                )
            name0 = str(replied_user.first_name)
            if is_approved(replied_user.id):
                disapprove_user(replied_user.id)
                await e.edit(
                    f"[{name0}](tg://user?id={replied_user.id}) `Rechazado para PM!`",
                )
                await asyncio.sleep(5)
                await e.delete()
            else:
                await e.edit(
                    f"[{name0}](tg://user?id={replied_user.id}) nunca fue aprobado!",
                )
                await asyncio.sleep(5)
                await e.delete()
        elif e.is_private:
            bbb = await e.get_chat()
            aname = await e.client.get_entity(bbb.id)
            if str(bbb.id) in DEVLIST:
                return await eor(
                    e,
                    "`Lol, él es mi desarrollador\nNo puede ser desaprobado.`",
                )
            name0 = str(aname.first_name)
            if is_approved(bbb.id):
                disapprove_user(bbb.id)
                await e.edit(f"[{name0}](tg://user?id={bbb.id}) `Rechazado para PM!`")
                await asyncio.sleep(5)
                await e.delete()
                if Var.LOG_CHANNEL:
                    await e.client.send_message(
                        Var.LOG_CHANNEL,
                        f"[{name0}](tg://user?id={bbb.id})Fue desaprobado para PM usted.",
                    )
            else:
                await e.edit(f"[{name0}](tg://user?id={bbb.id}) nunca fue aprobado!")
                await asyncio.sleep(5)
                await e.delete()
        else:
            await e.edit(NO_REPLY)

    @ultroid_cmd(
        pattern="block$",
    )
    async def blockpm(block):
        if block.reply_to_msg_id:
            reply = await block.get_reply_message()
            replied_user = await block.client.get_entity(reply.sender_id)
            aname = replied_user.id
            if str(aname) in DEVLIST:
                return await eor(
                    block,
                    "`Lol, él es mi desarrollador\nNo puede ser bloqueado`",
                )
            name0 = str(replied_user.first_name)
            await block.client(BlockRequest(replied_user.id))
            await block.edit("`Has sido bloqueado!`")
            uid = replied_user.id
        elif block.is_private:
            bbb = await block.get_chat()
            if str(bbb.id) in DEVLIST:
                return await eor(
                    block,
                    "`Lol, él es mi desarrollador\nNo puede ser bloqueado`",
                )
            await block.client(BlockRequest(bbb.id))
            aname = await block.client.get_entity(bbb.id)
            await block.edit("`Has sido bloqueado!`")
            name0 = str(aname.first_name)
            uid = bbb.id
        else:
            await block.edit(NO_REPLY)
        try:
            disapprove_user(uid)
        except AttributeError:
            pass
        if Var.LOG_CHANNEL:
            await block.client.send_message(
                Var.LOG_CHANNEL,
                f"#BLOCKEADO\nUser: [{name0}](tg://user?id={uid})",
            )

    @ultroid_cmd(
        pattern="unblock$",
    )
    async def unblockpm(unblock):
        if unblock.reply_to_msg_id:
            reply = await unblock.get_reply_message()
            replied_user = await unblock.client.get_entity(reply.sender_id)
            name0 = str(replied_user.first_name)
            await unblock.client(UnblockRequest(replied_user.id))
            await unblock.edit("`Has sido desbloqueado.`")
        else:
            await unblock.edit(NO_REPLY)
        if Var.LOG_CHANNEL:
            await unblock.client.send_message(
                Var.LOG_CHANNEL,
                f"[{name0}](tg://user?id={replied_user.id}) fue desbloqueado!.",
            )


@callback(
    re.compile(
        b"approve_(.*)",
    ),
)
@owner
async def apr_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if str(uid) in DEVLIST:
        await event.edit("¡Es un desarrollador! Aprobado!")
    if not is_approved(uid):
        approve_user(uid)
        try:
            user_name = (await ultroid.get_entity(uid)).first_name
        except BaseException:
            user_name = ""
        await event.edit(
            f"[{user_name}](tg://user?id={uid}) `aprobado para PM!`",
            buttons=[
                Button.inline("Disapprove PM", data=f"disapprove_{uid}"),
                Button.inline("Block", data=f"block_{uid}"),
            ],
        )
        async for message in ultroid.iter_messages(uid, search=UND):
            await message.delete()
        async for message in ultroid.iter_messages(uid, search=UNS):
            await message.delete()
        await event.answer("Approved.")
        x = await ultroid.send_message(uid, "¡Has sido aprobado para enviarme un PM!")
        await asyncio.sleep(5)
        await x.delete()
    else:
        await event.edit(
            "`El usuario ya puede ser aprobado.`",
            buttons=[
                Button.inline("Disapprove PM", data=f"disapprove_{uid}"),
                Button.inline("Block", data=f"block_{uid}"),
            ],
        )


@callback(
    re.compile(
        b"disapprove_(.*)",
    ),
)
@owner
async def disapr_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if is_approved(uid):
        disapprove_user(uid)
        try:
            user_name = (await ultroid.get_entity(uid)).first_name
        except BaseException:
            user_name = ""
        await event.edit(
            f"[{user_name}](tg://user?id={uid}) `desaprobado de PMs!`",
            buttons=[
                Button.inline("Approve PM", data=f"approve_{uid}"),
                Button.inline("Block", data=f"block_{uid}"),
            ],
        )
        await event.answer("DisApproved.")
        x = await ultroid.send_message(uid, "Se le ha desaprobado el envío de mensajes por correo electrónico!")
        await asyncio.sleep(5)
        await x.delete()
    else:
        await event.edit(
            "`El usuario nunca fue aprobado!`",
            buttons=[
                Button.inline("Disapprove PM", data=f"disapprove_{uid}"),
                Button.inline("Block", data=f"block_{uid}"),
            ],
        )


@callback(
    re.compile(
        b"block_(.*)",
    ),
)
@owner
async def blck_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    await ultroid(BlockRequest(uid))
    try:
        user_name = (await ultroid.get_entity(uid)).first_name
    except BaseException:
        user_name = ""
    await event.answer("Blocked.")
    await event.edit(
        f"[{user_name}](tg://user?id={uid}) ¡ha sido bloqueado!**",
        buttons=Button.inline("UnBlock", data=f"unblock_{uid}"),
    )


@callback(
    re.compile(
        b"unblock_(.*)",
    ),
)
@owner
async def unblck_in(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    await ultroid(UnblockRequest(uid))
    try:
        user_name = (await ultroid.get_entity(uid)).first_name
    except BaseException:
        user_name = ""
    await event.answer("UnBlocked.")
    await event.edit(
        f"[{user_name}](tg://user?id={uid}) ha sido **desbloqueado!**",
        buttons=[
            Button.inline("Block", data=f"block_{uid}"),
            Button.inline("Close", data="deletedissht"),
        ],
    )


@callback("deletedissht")
async def ytfuxist(e):
    await e.answer("Deleted.")
    await e.delete()


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
