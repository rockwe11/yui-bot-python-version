from discord.ext import commands

from dscommands.command_context import CommandContext


class SkipCommand:
    async def handle(self, ctx: CommandContext):
        vc = ctx.get_message().guild.voice_client
        if vc:
            if not vc.is_playing():
                ctx.send_message("Никакая музыка не играет")
                return
            if vc.queue.is_empty:
                await vc.stop()
                return
            await vc.seek(vc.track.length * 1000)
            if vc.is_paused():
                await vc.resume()
        else:
            await ctx.send_message("Я не подключена к голосовому каналу")
        # if voice_client.is_playing():
        #     await voice_client.stop()
        # else:
        #     await ctx.send_message("Никакая музыка не играет")

    def getName(self):
        return "skip"

    def get_help(self):
        return "Пропустить текущий трек в очереди\n\n" \
               "Использование: {prefix}skip"
