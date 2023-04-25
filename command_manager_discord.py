import wavelink
from discord import Message
from data import db_session
from data.users import User
from dscommands.command_context import CommandContext
from dscommands.games.bones_command import BonesCommand
from dscommands.games.coin_command import CoinCommand
from dscommands.games.sapper_command import SapperCommand
from dscommands.music.join_command import JoinCommand
from dscommands.music.leave_command import LeaveCommand
from dscommands.music.pause_command import PauseCommand
from dscommands.music.play_command import PlayCommand
from dscommands.music.resume_command import ResumeCommand
from dscommands.music.skip_command import SkipCommand
from dscommands.music.stop_command import StopCommand
from dscommands.profile.balance_command import BalanceCommand
from dscommands.profile.bonus_command import BonusCommand
from dscommands.utilities.help_command import HelpCommand
from dscommands.utilities.ping_command import PingCommand


class CommandManager:
    emojies = [
        "(´▽`ʃ♡ƪ)",
        "(o^▽^o)",
        "ヽ(・∀・)ﾉ",
        "(o･ω･o)",
        "(^人^)",
        "O(∩_∩)O",
        "(´• ω •)",
        "╰(▔∀▔)╯",
        "(✯◡✯)",
        "(⌒‿⌒)",
        "(*°▽°*)",
        "(´｡• ᵕ •｡)",
        "ヽ(>∀<☆)ノ",
        "＼(￣▽￣)／",
        "(o˘◡˘o)",
        "(╯✧▽✧)╯",
        "( ‾́ ◡ ‾́ )",
        "(๑˘︶˘๑)",
        "(´･ᴗ･ )",
        "`(*>﹏<*)′",
        "(⌒▽⌒)☆",
        "(´｡• ω •｡)",
        "(＠＾◡＾)",
        "(o´▽o)",
        "(＾▽＾)",
        "(─‿‿─)",
        "(◕‿◕)",
        "＼(≧▽≦)／",
        "٩(｡•́‿•̀｡)۶",
        "o(≧▽≦)o",
        "o(*^＠^*)o",
        "o(>ω<)o"
    ]

    def __init__(self, client):
        self.client = client

        self.client.loop.create_task(self.connect_nodes())

        self.commands = []
        self.add_command(PingCommand)
        self.add_command(BonesCommand)
        self.add_command(BalanceCommand)
        self.add_command(CoinCommand)
        self.add_command(SapperCommand)
        self.add_command(BonusCommand)
        self.add_command(HelpCommand)
        self.add_command(JoinCommand)
        self.add_command(PlayCommand)
        self.add_command(StopCommand)
        self.add_command(PauseCommand)
        self.add_command(ResumeCommand)
        self.add_command(LeaveCommand)
        self.add_command(SkipCommand)

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
            ctx = CommandContext(self, message, args, self.client)
            db_sess.close()
            await cmd.handle(ctx)

    async def connect_nodes(self):
        await self.client.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.client,
            host='0.0.0.0',
            port=2333,
            password='youshallnotpass'
        )
