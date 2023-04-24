import datetime
import random

from data import db_session
from data.users import User
from dscommands.command_context import CommandContext
import time


class BonusCommand:
    async def handle(self, ctx: CommandContext):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.did == ctx.get_message().author.id).first()
        bonustm = user.bonustm
        if bonustm <= datetime.datetime.now().timestamp():
            coins_to_add = 10000 + random.choice(range(20001))
            user.coins += coins_to_add
            user.bonustm = datetime.datetime.now().timestamp() + 43200
            db_sess.commit()
            db_sess.close()
            await ctx.send_message(f"💴 Вы получили бонус в размере {'{:,}'.format(coins_to_add).replace(',', '.')}!"
                                   "\nЧерез 12 часов Вы сможете получить бонус снова.")
        else:
            time_to_get = datetime.datetime.fromtimestamp(bonustm) - datetime.datetime.now()
            await ctx.send_message("💴 Вы сможете получить бонус через "
                                   f"{int(time_to_get.total_seconds() // 3600)} часов {int(time_to_get.total_seconds() % 3600 // 60)} минут")

    def getName(self):
        return "bonus"

    def get_help(self):
        return "Бонус в размере от 10000 до 30000 (раз в 12 часов).\n\n" \
               "Использование: {prefix}bonus"
