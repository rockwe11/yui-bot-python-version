import os

from discord.ext import commands

from command_manager_discord import CommandManager
from data import db_session
from data.guild_settings import GuildSettings
from data.users import User


class Listener(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} is ready')
        self.command_manager = CommandManager(self)

    async def on_message(self, message):
        db_sess = db_session.create_session()
        user_id = message.author.id
        guild_id = message.guild.id
        guild = db_sess.query(GuildSettings).get(guild_id)
        if not guild:
            guild = GuildSettings()
            guild.guildid = guild_id
            guild.prefix = os.getenv('PREFIX')
            guild.language = "1"
            db_sess.add(guild)
            db_sess.commit()
        user = db_sess.query(User).filter(User.did == user_id).first()
        if user:
            user.coins += 5
            db_sess.commit()
        content = message.content
        if content.startswith(guild.prefix):
            db_sess.close()
            await self.command_manager.handle(message, guild.prefix)
