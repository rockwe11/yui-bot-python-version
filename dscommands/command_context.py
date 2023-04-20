from discord import Message
from discord.ext import commands


class CommandContext:
    def __init__(self, message: Message, args, client: commands.bot):
        self.message = message
        self.args = args
        self.client = client

    def get_guild(self):
        return self.message.guild

    def get_message(self):
        return self.message

    def get_args(self):
        return self.args

    def get_client(self):
        return self.client

    async def send_message(self, msg):
        await self.message.channel.send(msg)

