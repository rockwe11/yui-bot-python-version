import random

from data import db_session
from data.users import User
from vkcommands.command_context import CommandContextVK


class CoinCommand:
    def handle(self, ctx: CommandContextVK):
        db_sess = db_session.create_session()
        player_id = ctx.get_event().message['from_id']
        user = db_sess.query(User).filter(User.vid == player_id).first()
        if len(ctx.get_args()) < 2:
            ctx.send_message("Недостаточно аргументов")
        elif not ctx.get_args()[0].isdigit():
            ctx.send_message("Первый аргумент должен быть целочисленным числом")
        elif int(ctx.get_args()[0]) > 1000000 or int(ctx.get_args()[0]) < 1000:
            ctx.send_message("Ставка должна быть в пределе от 1000 до 1000000")
        elif int(ctx.get_args()[0]) > user.coins:
            ctx.send_message("У Вас недостаточно монет")
        elif ctx.get_args()[1] not in ["орел", "орёл", "решка"]:
            ctx.send_message("На монете может выпасть либо \"Орел\", либо \"Решка\"")
        else:
            if ctx.get_args()[1] in ["орел", "орёл"]:
                bet = 0
            else:
                bet = 1
            res = random.choice(range(2))
            if res == bet:
                ctx.send_message(f"Вы угадали! {'Выпал орел.' if res == 0 else 'Выпала решка.'}\n💴 (+{ctx.get_args()[0]})")
                user.coins += int(ctx.get_args()[0])
                db_sess.commit()
            else:
                ctx.send_message(f"Вы не угадали. {'Выпал орел.' if res == 0 else 'Выпала решка.'}\n💴 (-{ctx.get_args()[0]})")
                user.coins -= int(ctx.get_args()[0])
                db_sess.commit()

    def getName(self):
        return "coin"

    def get_help(self):
        return "🪙 Игра \"Монетка\"\n" \
               "Симулятор популярной игры, в которой две личности выбирают сторону, орла, или решку, далее один из них подбрасывает монетку.\n" \
               "Победит тот, чья сторона монетки окажется кверху.\n\n" \
               "Использование: coin [ставка] [орел/решка]"
