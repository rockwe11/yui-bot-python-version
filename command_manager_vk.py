import json
import random

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotMessageEvent
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from data import db_session
from data.users import User
from vkcommands.command_context import CommandContextVK
from vkcommands.games.bones_command import BonesCommand
from vkcommands.games.coin_command import CoinCommand
from vkcommands.games.sapper_command import SapperCommand
from vkcommands.profile.balance_command import BalanceCommand
from vkcommands.profile.bonus_command import BonusCommand
from vkcommands.utilities.help_command import HelpCommand
from vkcommands.utilities.ping_command import PingCommand


class CommandManagerVK:
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

    def __init__(self, vk_client: VkApi):
        self.vk_client = vk_client
        self.commands = []
        self.add_command(PingCommand)
        self.add_command(HelpCommand)
        self.add_command(BalanceCommand)
        self.add_command(BonusCommand)
        self.add_command(BonesCommand)
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

    def handle(self, event: VkBotMessageEvent):
        split = event.obj.message['text'].lower().strip().split()
        invoke = split[0].lower()
        cmd = self.get_command(invoke)
        if not cmd and 'payload' in event.message:
            payload = json.loads(event.message['payload'])
            invoke = payload['command'] if 'command' in payload else None
            cmd = self.get_command(invoke)
            split = []
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.vid == event.obj.message['from_id']).first()
        if not user:
            user = User(vid=event.obj.message['from_id'], did="", coins=10000, bonustm=0, language='1')
            db_sess.add(user)
            db_sess.commit()
        db_sess.close()
        if cmd:
            args = []
            if len(split) > 1:
                args = split[1:]
            ctx = CommandContextVK(self, event, args, self.vk_client)
            cmd.handle(ctx)
        else:
            self.send_no_command(event)

    def send_no_command(self, event):
        # print(event.message)
        vk_keyboard = VkKeyboard(one_time=True)
        vk_keyboard.add_button("📚 Помощь", color=VkKeyboardColor.PRIMARY, payload={'command': 'help'})
        self.vk_client.get_api().messages.send(user_id=event.obj.message['from_id'],
                                               message=f"{random.choice(self.emojies)} Я не знаю такой команды!",
                                               keyboard=vk_keyboard.get_keyboard(),
                                               random_id=random.randint(0, 2 ** 64))
