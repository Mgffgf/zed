# ZedMusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from ZedMusic.config import SUDO_USERS
from ZedMusic.services.callsmusic.callsmusic import client as USER


@Client.on_message(filters.command(["اذاعه"]))
async def broadcast(_, message: Message):
    sent = 0
    failed = 0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("**␥┆جـاري اذاعـة الرسـاله .. 📨**")
        if not message.reply_to_message:
            await wtf.edit("**␥┆بالـرد عـلى الرسـاله .. لــ الاذاعـه🧧**")
            return
        lmao = message.reply_to_message.text
        async for dialog in USER.iter_dialogs():
            try:
                await USER.send_message(dialog.chat.id, lmao)
                sent = sent + 1
                await wtf.edit(
                    f"**␥┆تمـت الاذاعـة .. بنجـاح 📤☑️**\n\n**␥┆تم الارسـال الـى:** `{sent}` دردشـه\n**␥┆اخفـق الارسـال الـى:** {failed} دردشـه"
                )
                await asyncio.sleep(3)
            except:
                failed = failed + 1
                # await wtf.edit(f"`broadcasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")

        await message.reply_text(
            f"**␥┆تمـت الاذاعـة .. بنجـاح 📤☑️**\n\n**␥┆تم الارسـال الـى:** `{sent}` دردشـه\n**␥┆اخفـق الارسـال الـى:** {failed} دردشـه"
        )
