from discord import Message
from discord.ext import commands


class CommandContext:
    def __init__(self, command_manager, message: Message, args, client: commands.bot):
        self.command_manager = command_manager
        self.message = message
        self.args = args
        self.client = client

    def get_command_manager(self):
        return self.command_manager

    def get_guild(self):
        return self.message.guild

    def get_message(self):
        return self.message

    def get_args(self):
        return self.args

    def get_client(self):
        return self.client

    async def send_message(self, msg, **kwargs):
        await self.message.channel.send(msg, **kwargs)

