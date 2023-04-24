from data import db_session
from data.users import User
from vkcommands.command_context import CommandContextVK


class BalanceCommand:
    def handle(self, ctx: CommandContextVK):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.vid == ctx.get_event().message['from_id']).first()
        ctx.send_message(f"💴 Ваш текущий баланс: {'{:,}'.format(user.coins).replace(',', '.')}")

    def getName(self):
        return "balance"

    def get_help(self):
        return "Данная команда показывает текущий баланс Вашего аккаунта.\n\n" \
               "Использование: balance"
