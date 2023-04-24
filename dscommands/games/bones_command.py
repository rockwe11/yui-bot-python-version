import random

from data.users import User
from dscommands.command_context import CommandContext
from data import db_session
from random import choice


class BonesCommand:
    async def handle(self, ctx: CommandContext):
        db_sess = db_session.create_session()
        player_id = ctx.get_message().author.id
        user = db_sess.query(User).filter(User.did == player_id).first()
        if len(ctx.get_args()) < 1:
            await ctx.send_message("Недостаточно аргументов")
        elif not ctx.get_args()[0].isdigit():
            await ctx.send_message("Аргумент должен быть целочисленным числом")
        elif int(ctx.get_args()[0]) > 1000000 or int(ctx.get_args()[0]) < 1000:
            await ctx.send_message("Ставка должна быть в пределе от 1000 до 1000000")
        elif int(ctx.get_args()[0]) > user.coins:
            await ctx.send_message("У Вас недостаточно монет")
        else:
            res1, res2 = random.choice(range(1, 13)), random.choice(range(1, 13))
            if res1 > res2:
                coins = int(int(ctx.get_args()[0]) * (res1 / res2))
                await ctx.send_message(f"🎲 У Вас {res1} костей, у меня {res2}.\nВы выиграли! 💴 (+{coins})")
                user.coins += coins
                db_sess.commit()
            elif res1 < res2:
                coins = int(int(ctx.get_args()[0]) / (res2 / res1))
                await ctx.send_message(f"🎲 У Вас {res1} костей, у меня {res2}.\nВы проиграли. 💴 (-{coins})")
                user.coins -= coins
                db_sess.commit()
            else:
                await ctx.send_message(f"🎲 У Вас {res1} костей, у меня {res2}.\nНичья!")

            # await ctx.send_message(random.choice(range(13)))

    def getName(self):
        return "bones"

    def get_help(self):
        return "Игра « Кости »\n" \
               "Использование: {prefix}bones [ставка]"
