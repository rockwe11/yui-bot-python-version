import random

from data import db_session
from data.users import User
from dscommands.command_context import CommandContext


class CoinCommand:
    async def handle(self, ctx: CommandContext):
        db_sess = db_session.create_session()
        player_id = ctx.get_message().author.id
        user = db_sess.query(User).filter(User.did == player_id).first()
        if len(ctx.get_args()) < 2:
            await ctx.send_message("Недостаточно аргументов")
        elif not ctx.get_args()[0].isdigit():
            await ctx.send_message("Первый аргумент должен быть целочисленным числом")
        elif int(ctx.get_args()[0]) > 1000000 or int(ctx.get_args()[0]) < 1000:
            await ctx.send_message("Ставка должна быть в пределе от 1000 до 1000000")
        elif int(ctx.get_args()[0]) > user.coins:
            await ctx.send_message("У Вас недостаточно монет")
        elif ctx.get_args()[1] not in ["орел", "орёл", "решка"]:
            await ctx.send_message("На монете может выпасть либо \"Орел\", либо \"Решка\"")
        else:
            if ctx.get_args()[1] in ["орел", "орёл"]:
                bet = 0
            else:
                bet = 1
            res = random.choice(range(2))
            if res == bet:
                await ctx.send_message(f"Вы угадали! {'Выпал орел.' if res == 0 else 'Выпала решка.'}\n💴 (+{ctx.get_args()[0]})")
                user.coins += int(ctx.get_args()[0])
                db_sess.commit()
            else:
                await ctx.send_message(f"Вы не угадали. {'Выпал орел.' if res == 0 else 'Выпала решка.'}\n💴 (-{ctx.get_args()[0]})")
                user.coins -= int(ctx.get_args()[0])
                db_sess.commit()

    def getName(self):
        return "coin"
