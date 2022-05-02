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
from pyrogram.errors import UserAlreadyParticipant

from ZedMusic.config import SUDO_USERS
from ZedMusic.helpers.decorators import authorized_users_only, errors
from ZedMusic.services.callsmusic import client as USER


@Client.on_message(filters.command(["دخول"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>قـم برفعـي مشـرفـاً في هـذه المجموعـه اولاً</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "ZedMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "**•♪╎تـم انضمامي لهـذه المجموعـه .. بنجـاح ⎙**")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>الحسـاب المساعـد بالتأكيـد في هـذه المجموعـه</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 خـــطـــأ 🛑 \n␥┆اخفق {user.first_name} من الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام لـ الحسـاب المسـاعد! تأكد من عدم حظر المستخدم في المجموعـة."
            "\n\n␥┆أو قـم باضافـة الحسـاب المسـاعد يدويـاً إلى مجموعتك وحاول مرة أخرى</b>",
        )
        return
    await message.reply_text(
        "<b>␥┆تـم انضمـام الحسـاب المسـاعد الـى المجموعـه .. بنجـاح ☑️</b>",
    )


@USER.on_message(filters.group & filters.command(["غادر"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>لا يمكن للمستخدم مغادرة مجموعتك! قد يكون هنـالك خطـأ."
            "\n\nأو اطردني يدويـاً من المجموعـة الخاصة بك</b>",
        )
        return


@Client.on_message(filters.command(["مغادره الكل"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("**␥┆جـاري .. مغـادرة الحسـاب المسـاعد من جميـع المجموعـات والقنـوات ...**")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"**✔️┆تم مغـادرة الحسـاب المسـاعد من :** {left} **دردشـه.**\n**✖️┆اخفـق في المغـادره من :** {failed} **دردشـه.**"
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"**✔️┆تم مغـادرة الحسـاب المسـاعد من :** {left} **دردشـه.**\n**✖️┆اخفـق في المغـادره من :** {failed} **دردشـه.**"
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Left {left} chats. Failed {failed} chats."
        )


@Client.on_message(
    filters.command(["انضمام", "انضم"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>␥┆قـم باضافتـي ادمن فـي القنـاة اولاً</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "ZedMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "**␥┆لقـد انضممت هنـا كمـا طلبت .. عزيـزي**")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>␥┆الحسـاب المسـاعد مـوجود بالفعـل .. بالقنـاة ☑️</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 خـــطـــأ 🛑 \n␥┆اخفق {user.first_name} من الانضمام إلى قنـاتك بسبب كثرة طلبات الانضمام لـ الحسـاب المسـاعد! تأكد من عدم حظر المستخدم في القنـاة."
            "\n\n␥┆أو قـم باضافـة الحسـاب المسـاعد يدويـاً إلى قنـاتك وحاول مرة أخرى</b>",
        )
        return
    await message.reply_text(
        "<b>␥┆لقـد تم انضمـام الحسـاب المسـاعد الى قناتـك .. بنجـاح ☑️</b>",
    )
