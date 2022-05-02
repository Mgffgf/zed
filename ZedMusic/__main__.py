import requests
from pyrogram import Client as Bot

from ZedMusic.config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN
from ZedMusic.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="ZedMusic.modules"),
)

bot.start()
run()
