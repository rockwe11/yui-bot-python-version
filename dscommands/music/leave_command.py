from discord.ext import commands

from dscommands.command_context import CommandContext
from dscommands.music.player import Player


class LeaveCommand:
    async def handle(self, ctx: CommandContext):
        vc = ctx.get_message().guild.voice_client
        if vc:
            if vc.is_connected():
                await vc.disconnect()
            else:
                await ctx.send_message("Я не в голосовом канале")
        else:
            await ctx.send_message("Я не подключена к голосовому каналу")

    def getName(self):
        return "leave"

    def get_help(self):
        return "Выйти из голосового канала\n\n" \
               "Использование: {prefix}leave"
