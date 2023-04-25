from data import db_session
from data.users import User
from dscommands.games.sapper.Player import Player
from vkcommands.command_context import CommandContextVK


class SapperCommand:
    numbers = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣"
    ]

    sessions = []

    def handle(self, ctx: CommandContextVK):
        player_id = ctx.get_event().message['from_id']
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.vid == player_id).first()
        if len(ctx.get_args()) > 0 and not self.get_player(player_id):
            if not ctx.get_args()[0].isdigit():
                ctx.send_message("❌ Первый аргумент должен быть целочисленным числом")
            elif int(ctx.get_args()[0]) > 1000000 or int(ctx.get_args()[0]) < 1000:
                ctx.send_message("❌ Ставка должна быть в пределе от 1000 до 1000000")
            elif int(ctx.get_args()[0]) > user.coins:
                ctx.send_message("❌ У Вас недостаточно монет")
            else:
                self.new_player(player_id, int(ctx.get_args()[0]))
                text_to_send = f"Вы начали новую игру.\nВаша ставка: {int(ctx.get_args()[0])}💴\n\n"
                user.coins -= int(ctx.get_args()[0])
                db_sess.commit()
                self.send_field(player_id, text_to_send, ctx)
        elif len(ctx.get_args()) >= 2 and ctx.get_args()[0] != "fl" and self.get_player(player_id):
            if not ctx.get_args()[0].isdigit() or not ctx.get_args()[1].isdigit():
                ctx.send_message("❌ Аргументы должны быть целочисленными числами")
            elif not(1 <= int(ctx.get_args()[0]) <= 5) or not(1 <= int(ctx.get_args()[1]) <= 5):
                ctx.send_message("❌ Размер поля - 5x5")
            else:
                x, y = int(ctx.get_args()[0]) - 1, int(ctx.get_args()[1]) - 1
                lose = self.get_player(player_id).open_cell(x, y)
                if lose:
                    text_to_send = f"Вы проиграли. (-{self.get_player(player_id).bet})\n\n"
                    self.send_field(player_id, text_to_send, ctx)
                    self.delete_player(player_id)
                else:
                    text_to_send = f"Вы открыли клетку\n\n"
                    self.send_field(player_id, text_to_send, ctx)
        elif len(ctx.get_args()) >= 3 and ctx.get_args()[0] == "fl" and self.get_player(player_id):
            if not ctx.get_args()[1].isdigit() or not ctx.get_args()[2].isdigit():
                ctx.send_message("❌ Аргументы должны быть целочисленными числами")
            elif not(1 <= int(ctx.get_args()[1]) <= 5) or not(1 <= int(ctx.get_args()[2]) <= 5):
                ctx.send_message("❌ Размер поля - 5x5")
            else:
                x, y = int(ctx.get_args()[1]) - 1, int(ctx.get_args()[2]) - 1
                text_to_send = self.get_player(player_id).set_flag(x, y)
                true_flags = 0
                if self.get_player(player_id).flC == 5:
                    for cX in range(5):
                        for cY in range(5):
                            if self.get_player(player_id).get_cell(cX, cY).is_flag() and self.get_player(player_id).get_cell(cX, cY).is_mine:
                                true_flags += 1
                if true_flags == 5:
                    text_to_send += f"Вы выиграли! (+{self.get_player(player_id).bet})\n\n"
                    self.get_player(player_id).open_all_cells()
                    self.send_field(player_id, text_to_send, ctx)
                    user.coins += 2 * self.get_player(player_id).bet
                    db_sess.commit()
                    self.delete_player(player_id)
                else:
                    text_to_send += "\n"
                    self.send_field(player_id, text_to_send, ctx)
        db_sess.close()

    def getName(self):
        return "sapper"

    def get_help(self):
        return "🧩 Игра « Сапёр »\n\n" \
               "sapper [Ставка] - начать игру\n" \
               "sapper [X] [Y] - открыть клетку\n" \
               "sapper fl [X] [Y] - установить флажок\n\n" \
               "🧩 Информация об игре « Сапёр »:\n\n" \
               "На игру дается 10 минут.\n" \
               "Для победы необходимо поставить все 5 флажков на все 5 бомб.\n" \
               "Поле: 5 на 5 клеток."

    def get_player(self, player_id) -> Player:
        for session in self.sessions:
            if session.get_player_id() == player_id:
                return session
        return None

    def new_player(self, player_id, bet):
        self.sessions.append(Player(player_id, bet))

    def delete_player(self, player_id):
        for i in range(len(self.sessions)):
            if self.sessions[i].player_id == player_id:
                self.sessions.pop(i)
                break

    def send_field(self, player_id, text_to_send, ctx):
        for height in range(6):
            text_to_send += self.numbers[height]
            for width in range(5):
                if height == 0:
                    text_to_send += self.numbers[width + 1]
                else:
                    if self.get_player(player_id).get_cell(width, height - 1).is_open\
                            or self.get_player(player_id).get_cell(width, height - 1).is_flag():
                        text_to_send += self.get_player(player_id).get_cell(width, height - 1).get_symb()
                    else:
                        text_to_send += "⏹"
            text_to_send += "\n"
        ctx.send_message(text_to_send)
