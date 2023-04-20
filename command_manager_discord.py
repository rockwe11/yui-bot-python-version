from discord import Message
from data import db_session
from data.users import User
from dscommands.command_context import CommandContext
from dscommands.games.bones_command import BonesCommand
from dscommands.games.coin_command import CoinCommand
from dscommands.games.sapper_command import SapperCommand
from dscommands.profile.balance_command import BalanceCommand
from dscommands.utilities.ping_command import PingCommand


class CommandManager:
    commands = []

    def __init__(self, client):
        self.client = client
        self.add_command(PingCommand)
        self.add_command(BonesCommand)
        self.add_command(BalanceCommand)
        self.add_command(CoinCommand)
        self.add_command(SapperCommand)

    def add_command(self, cmd):
        if cmd in self.commands or any([x.getName() == cmd().getName() for x in self.commands]):
            raise AssertionError("A command with this name is already present")
        else:
            self.commands.append(cmd())

    def get_command(self, invoke):
        for cmd in self.commands:
            if cmd.getName() == invoke:
                return cmd
        return None

    async def handle(self, message: Message, prefix):
        split = message.content.lower().replace(prefix, "", 1).split()
        invoke = split[0].lower()
        cmd = self.get_command(invoke)
        if cmd:
            await message.channel.typing()
            args = []
            if len(split) > 1:
                args = split[1:]
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.did == message.author.id).first()
            if not user:
                user = User(did=message.author.id, vid="", coins=10000, bonustm=0, language='1')
                db_sess.add(user)
                db_sess.commit()
            ctx = CommandContext(message, args, self.client)
            await cmd.handle(ctx)
