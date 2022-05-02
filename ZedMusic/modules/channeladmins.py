# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

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


from asyncio import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from ZedMusic.function.admins import set
from ZedMusic.helpers.decorators import authorized_users_only, errors
from ZedMusic.services.callsmusic import callsmusic
from ZedMusic.services.queues import queues
from ZedMusic.config import que


@Client.on_message(
    filters.command(["المؤقت", "مؤقتت"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def pause(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    chat_id = chid
    (
        await message.reply_text("ايقاف مؤقت ▶️")
    ) if (
        callsmusic.pause(chat_id)
    ) else (
        await message.reply_text("␥┆لا يـوجد شيء لـ ايقـافـه!❗")
    )


@Client.on_message(
    filters.command(["الاستئناف", "استئنافف"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def resume(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    chat_id = chid
    (
       await message.reply_text("استئنـاف ⏸")
    ) if (
        callsmusic.resume(chat_id)
    ) else (
        await message.reply_text("␥┆لا يـوجد شيء لـ استئنـافه!❗")
    )
        
    

@Client.on_message(
    filters.command(["الايقاف", "ايقافف"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("␥┆لا يـوجد شيء تحت التشغيـل!❗")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.stop(chat_id)
        await message.reply_text("␥┆تـم ايقـاف التشغيـل! ⏹")


@Client.on_message(
    filters.command(["التالي", "تاليي"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("␥┆لا يـوجد شيء لايقـافه مؤقتـاً!❗")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- تـم الايقاف **{skip[0]}**\n- قـم بتشغيل **{qeue[0][0]}**")
    
    
@Client.on_message(
    filters.command(["الكتم", "كتم"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def mute(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return 
    chat_id = chid
    result = await callsmusic.mute(chat_id)
    (
        await message.reply_text(" تـم الكتم .. بنجـاح ✅")
    ) if (
        result == 0
    ) else (
        await message.reply_text(" العضـو بالفعـل مكتوم ❌")
    ) if (
        result == 1
    ) else (
        await message.reply_text(" العضـو ليـس متصـل ❌")
    )
        
        
@Client.on_message(
    filters.command(["الغاء الكتم", "الغاء كتم"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return 
    chat_id = chid
    result = await callsmusic.unmute(chat_id)
    (
        await message.reply_text(" تـم الغـاء كتمـه .. بنجـاح✅")
    ) if (
        result == 0
    ) else (
        await message.reply_text("  العضـو ليـس مكتوم ❌")
    ) if (
        result == 1
    ) else (
        await message.reply_text(" العضـو ليـس متصـل ❌")
    )


@Client.on_message(filters.command("تحديث المشرفين"))
@errors
async def admincache(client, message: Message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**␥┆هل هـذه القنـاة مرتبطـة بالحسـاب...**")
        return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("**␥┆تم تحديث قائمـة المشـرفين ..  بنجـاح ❇️**")
