from discord.ext import commands

from dscommands.command_context import CommandContext
from dscommands.music.player import Player


class JoinCommand:
    async def handle(self, ctx: CommandContext):
        if not ctx.get_message().author.voice:
            await ctx.send_message("Вы не подключены к голосовому каналу")
            return
        channel = ctx.get_message().author.voice.channel
        await channel.connect(cls=Player())

    def getName(self):
        return "join"

    def get_help(self):
        return "Подключиться к голосовому каналу\n\n" \
               "Использование: {prefix}join"
