import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from event_listener import Listener
from data import db_session

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client = Listener(command_prefix="$", intents=intents)


class YLBotClient(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')


# @client.event
# async def on_message(msg):
#     print(msg.content)


client.add_command(ping)
db_session.global_init("db/yuibot.db")
client.run(TOKEN)
# client.add_command(ping)
