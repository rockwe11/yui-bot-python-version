import random
import threading

import discord
import os
from dotenv import load_dotenv
from vk_api import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from event_listener import Listener
from data import db_session
from event_listener_vk import ListenerVK

load_dotenv()
TOKEN = os.getenv('TOKEN')
VK_TOKEN = os.getenv('VK_TOKEN')
GROUP_ID = os.getenv('GROUP_ID')
db_session.global_init("db/yuibot.db")

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
listener_vk = ListenerVK(longpoll, vk_session)
threading.Thread(target=listener_vk.message_listener).start()

intents = discord.Intents.default()
intents.message_content = True
client = Listener(command_prefix="$", intents=intents)
client.run(TOKEN)

