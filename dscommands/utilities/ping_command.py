from discord.ext import commands

from dscommands.command_context import CommandContext


class PingCommand:
    async def handle(self, ctx: CommandContext):
        await ctx.get_message().channel.send(f"Пинг: {round(ctx.get_client().latency * 1000)}ms")

    def getName(self):
        return "ping"

    def get_help(self):
        return "Данная команда показывает задержку между сервером и ботом.\n\n" \
               "Использование: {prefix}ping"
