from discord.ext import commands

from dscommands.command_context import CommandContext


class StopCommand:
    async def handle(self, ctx: CommandContext):
        vc = ctx.get_message().guild.voice_client
        if vc:
            if vc.is_playing():
                await vc.stop()
            else:
                await ctx.send_message("Никакая музыка не играет")
        else:
            await ctx.send_message("Я не подключена к голосовому каналу")

    def getName(self):
        return "stop"

    def get_help(self):
        return "Прекратить воспроизведение музыки\n\n" \
               "Использование: {prefix}stop"
