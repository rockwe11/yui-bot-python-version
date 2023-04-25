from discord.ext import commands

from dscommands.command_context import CommandContext


class PauseCommand:
    async def handle(self, ctx: CommandContext):
        vc = ctx.get_message().guild.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
                await ctx.send_message("Музыка приостановлена")
            else:
                await ctx.send_message("Ничего не играет")
        else:
            await ctx.send_message("Я не подключена к голосовому каналу")
        # if voice_client.is_playing():
        #     await voice_client.pause()
        # else:
        #     await ctx.send_message("Музыка уже на паузе или вообще не играет")

    def getName(self):
        return "pause"

    def get_help(self):
        return "Приостановить музыку\n\n" \
               "Использование: {prefix}pause"
