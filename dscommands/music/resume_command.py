from discord.ext import commands

from dscommands.command_context import CommandContext


class ResumeCommand:
    async def handle(self, ctx: CommandContext):
        vc = ctx.get_message().guild.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
                await ctx.send_message("Музыка включена")
            else:
                await ctx.send_message("Музыка не остановлена")
        else:
            await ctx.send_message("Я не подключена к голосовому каналу")
        # if voice_client.is_paused():
        #     await voice_client.resume()
        # else:
        #     await ctx.send_message("Музыка не играет")

    def getName(self):
        return "resume"

    def get_help(self):
        return "Продолжить музыку\n\n" \
               "Использование: {prefix}resume"
