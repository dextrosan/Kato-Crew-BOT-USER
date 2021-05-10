

from . import *

REPOMSG = (
    "• **AL CAPONE  USERBOT** •\n\n",
    "• Support - @Dextrov",
)


@ultroid_cmd(pattern="repo$")
async def repify(e):
    try:
        q = await ultroid_bot.inline_query(asst.me.username, "repo")
        await q[0].click(e.chat_id)
        if e.sender_id == ultroid_bot.uid:
            await e.delete()
    except ChatSendInlineForbiddenError or bmi:
        await eor(e, REPOMSG)
