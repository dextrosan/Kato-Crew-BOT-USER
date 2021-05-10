

"""
✅ Comandos by: @Dextrov -

• `{i}addsudo`
    Agregar usuarios de Sudo respondiendo al usuario o usando <space> apartado userid(s)

• `{i}delsudo`
    Elimine usuarios de Sudo respondiendo al usuario o usando <space> separated userid(s)

• `{i}listsudo`
    Lista de todos los usuarios de sudo.
"""


from pyUltroid.misc._decorators import sed

from . import *


@ultroid_cmd(
    pattern="addsudo ?(.*)",
)
async def _(ult):
    inputs = ult.pattern_match.group(1)
    if Var.BOT_MODE:
        try:
            if ult.sender_id != int(Redis(OWNER_ID)):
                return await eod(ult, "`Los usuarios de sudo no pueden agregar nuevos sudos.!`", time=10)
        except BaseException:
            pass
    else:
        if ult.sender_id != ultroid_bot.uid:
            return await eod(ult, "`Los usuarios de udo no pueden agregar nuevos sudos.!`", time=10)
    ok = await eor(ult, "`Actualización de la lista de usuarios de SUDO ...`")
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        sed.append(id)
        mmm = ""
        if id == ultroid_bot.me.id:
            mmm += "No puede agregarse a sí mismo como usuario Sudo..."
        elif is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `Ya es usuario de SUDO ...`"
        elif add_sudo(id):
            udB.set("SUDO", "True")
            mmm += f"**Added [{name}](tg://user?id={id}) as SUDO User**"
        else:
            mmm += "`PARECE QUE ESTA FUNCIÓN ELIGE ROMPERSE`"
        await eod(ok, mmm, time=5)

    if inputs:
        id = await get_user_id(inputs)
        try:
            name = (await ult.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
        sed.append(id)
        mmm = ""
        if id == ultroid_bot.me.id:
            mmm += "No puede agregarse a sí mismo como usuario Sudo..."
        elif is_sudo(id):
            if name != "":
                mmm += f"[{name}](tg://user?id={id}) `Ya es usuario de SUDO ...`"
            else:
                mmm += f"`{id} Ya es usuario de SUDO...`"
        elif add_sudo(id):
            udB.set("SUDO", "True")
            if name != "":
                mmm += f"**Agregado [{name}](tg://user?id={id}) como usuario de SUDO**"
            else:
                mmm += f"**Agregado **`{id}`** como usuario de SUDO**"
        else:
            mmm += "`PARECE QUE ESTA FUNCIÓN ELIGE ROMPERSE`"
        await eod(ok, mmm, time=5)
    else:
        return await eod(ok, "`Responder a un mensaje o agregar su id/username.`", time=5)


@ultroid_cmd(
    pattern="delsudo ?(.*)",
)
async def _(ult):
    inputs = ult.pattern_match.group(1)
    if Var.BOT_MODE:
        try:
            if ult.sender_id != int(Redis(OWNER_ID)):
                return await eod(
                    ult,
                    "Eres usuario de sudo, no puedes agregar otro usuario de sudo.",
                    time=5,
                )
        except BaseException:
            pass
    else:
        if ult.sender_id != ultroid_bot.uid:
            return await eor(ult, "Eres usuario de sudo, no puedes agregar otro usuario de sudo.")
    ok = await eor(ult, "`Actualización de la lista de usuarios de SUDO ...`")
    if ult.reply_to_msg_id:
        replied_to = await ult.get_reply_message()
        id = await get_user_id(replied_to.sender_id)
        name = (await ult.client.get_entity(int(id))).first_name
        sed.remove(id)
        mmm = ""
        if not is_sudo(id):
            mmm += f"[{name}](tg://user?id={id}) `wasn't a SUDO User ...`"
        elif del_sudo(id):
            mmm += f"**Removido [{name}](tg://user?id={id}) Del usuario de SUDO(s)**"
        else:
            mmm += "`PARECE QUE ESTA FUNCIÓN ELIGE ROMPERSE`"
        await eod(ok, mmm, time=5)

    if inputs:
        id = await get_user_id(inputs)
        try:
            name = (await ult.client.get_entity(int(id))).first_name
        except BaseException:
            name = ""
        sed.remove(id)
        mmm = ""
        if not is_sudo(id):
            if name != "":
                mmm += f"[{name}](tg://user?id={id}) `wasn't a SUDO User ...`"
            else:
                mmm += f"`{id} no era un usuario de SUDO...`"
        elif del_sudo(id):
            if name != "":
                mmm += f"**Removed [{name}](tg://user?id={id}) from SUDO User(s)**"
            else:
                mmm += f"**Removed **`{id}`** from SUDO User(s)**"
        else:
            mmm += "`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`"
        await eod(ok, mmm, time=5)


@ultroid_cmd(
    pattern="listsudo$",
)
async def _(ult):
    ok = await eor(ult, "`...`")
    sudos = Redis("SUDOS")
    if sudos == "" or sudos is None:
        return await eod(ult, "`No SUDO User was assigned ...`", time=5)
    sumos = sudos.split(" ")
    msg = ""
    for i in sumos:
        try:
            name = (await ult.client.get_entity(int(i))).first_name
        except BaseException:
            name = ""
        if name != "":
            msg += f"• [{name}](tg://user?id={i}) ( `{i}` )\n"
        else:
            msg += f"• `{i}` -> Invalid User\n"
    m = udB.get("SUDO") if udB.get("SUDO") else "False"
    if m == "False":
        m = "[False](https://telegra.ph/Ultroid-04-06)"
    return await ok.edit(
        f"**SUDO MODE : {m}\n\nList of SUDO Users :**\n{msg}", link_preview=False
    )


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
