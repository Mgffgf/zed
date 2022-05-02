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

from pyrogram import Client, filters
from pyrogram.types import Message

from ZedMusic.config import PMPERMIT, SUDO_USERS
from ZedMusic.services.callsmusic import client as USER

PMSET = True
pchats = []


@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    if PMPERMIT == "ENABLE":
        if PMSET:
            chat_id = message.chat.id
            if chat_id in pchats:
                return
            await USER.send_message(
                message.chat.id,
                "**␥┆مرحبـاً .. انـا الحسـاب المسـاعد لبـوت تشغيل الاغـاني في المكالمـات .\n\n**␥┆القـوانين :**\n   - لا يسمح بالدردشـه معـي فـ انـا لسـت مجـرد شخـص\n   - لاتكـرر رسائـلك فقـط ارسـل وانتظـر الـرد\n\n**␥┆ارسـل رابـط المجمـوعه او القنـاة أو معـرف المستخـدم إذا لم يتمكن الحسـاب من الانضمـام إلى مجمـوعتك او قنـاتك.**\n\n**⚠️┆مـلاحظـه :**\n   - اذا راسلتني ، فهذا يعني أن الحسـاب سيرى رسالتك وينضـم الى الدردشـه تلقائيـاً...\n\n",
            )
            return


@Client.on_message(filters.command(["/الحمايه"]))
async def bye(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        global PMSET
        text = message.text.split(" ", 1)
        queryy = text[1]
        if queryy == "تفعيل":
            PMSET = True
            await message.reply_text("**␥┆تـم تفعيـل الحمـايه .. بنجـاح 🔐☑️**")
            return
        if queryy == "تعطيل":
            PMSET = None
            await message.reply_text("**␥┆تـم تعطيـل الحمـايه .. بنجـاح 🔓☑️**")
            return


@USER.on_message(filters.text & filters.private & filters.me)
async def autopmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("**␥┆سيتـم تفعيـل PM بسبب الرسائـل الصـادرة..**")
        return
    message.continue_propagation()


@USER.on_message(filters.command("سماح", [".", ""]) & filters.me & filters.private)
async def pmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("**␥┆تـم السمـاح لــ وضـع PM .. بنجـاح ☑️**")
        return
    message.continue_propagation()


@USER.on_message(filters.command("رفض", [".", ""]) & filters.me & filters.private)
async def rmpmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if chat_id in pchats:
        pchats.remove(chat_id)
        await message.reply_text("**␥┆تـم الرفـض لــ وضـع PM .. بنجـاح ☑️**")
        return
    message.continue_propagation()
