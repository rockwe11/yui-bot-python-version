from data import db_session
from data.users import User
from dscommands.command_context import CommandContext


class BalanceCommand:
    async def handle(self, ctx: CommandContext):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.did == ctx.get_message().author.id).first()
        await ctx.send_message(f"💴 Ваш текущий баланс: {'{:,}'.format(user.coins).replace(',', '.')}")

    def getName(self):
        return "balance"

    def get_help(self):
        return "Данная команда показывает текущий баланс Вашего аккаунта.\n\n" \
               "Использование: {prefix}balance"
