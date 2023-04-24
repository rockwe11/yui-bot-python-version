import random

import discord
from discord import Guild
from discord.ext import commands

from data import db_session
from data.guild_settings import GuildSettings
from dscommands.command_context import CommandContext


class HelpCommand:
    async def handle(self, ctx: CommandContext):
        # await ctx.get_message().channel.send(f"Пинг: {round(ctx.get_client().latency * 1000)}ms")
        db_sess = db_session.create_session()
        prefix = db_sess.query(GuildSettings).filter(GuildSettings.guildid == ctx.get_message().guild.id).first().prefix
        db_sess.close()
        if len(ctx.get_args()) > 0:
            command_name = ctx.get_args()[0]
            command = ctx.command_manager.get_command(command_name)
            if command:
                await ctx.send_message(command.get_help().format(prefix=prefix))
            else:
                await ctx.send_message(f"{random.choice(ctx.command_manager.emojies)} Я не знаю такой команды!")
        else:
            embed = discord.Embed(title="Используйте $help [имя команды] для расширенной информации",
                                  color=0xf9814e)
            for command in ctx.command_manager.commands:
                embed.add_field(name="", value=f"{prefix}{command.getName()}", inline=False)
            embed.set_footer(text='© YuiBot')
            await ctx.send_message("", embed=embed)

            # text_to_send = "📚 Список доступных команд:\n\n"
            # for command in ctx.command_manager.commands:
            #     text_to_send += command.getName() + "\n"
            # ctx.send_message(text_to_send)

    def getName(self):
        return "help"

    def get_help(self):
        return "Данная команда показывает список команд бота.\n\n" \
               "Использование: {prefix}help [Название команды]"
