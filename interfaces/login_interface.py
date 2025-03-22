import click
from helpers.validator import InputValidation as Validator
from db.storage import AuthService, Session
from core.generator import PasswordGenerator
from translation import Language
from i18n import t

class Authorization:
    __user_auth = False

    @staticmethod
    def register():
        """Регистрация нового пользователя."""
        username = click.prompt(t("LoginInterface.Register.RegisterUsername"), type=str)
        username = Validator.validate_username(username)

        gen_master_pass = click.confirm(t("LoginInterface.Register.RegisterPassword"), default=True)
        if gen_master_pass:
            master_password = PasswordGenerator.generate(16, 2)
            click.echo(t("LoginInterface.Register.YourMasterPassword") + click.style(master_password, fg="green"))
        else:
            master_password = click.prompt(
                t("LoginInterface.Register.CreateMasterPassword"),
                hide_input=True,
                confirmation_prompt=True
            )
            master_password = Validator.validate_password(master_password)

        if AuthService.register(username, master_password):
            click.secho(t("LoginInterface.Register.SuccessfulRegister"), fg="green")

    @staticmethod
    def login():
        """Авторизация пользователя."""
        username = click.prompt(t("LoginInterface.Login.EnterName"), type=str)
        username = Validator.validate_username(username)

        master_password = click.prompt(
            t("LoginInterface.Login.EnterMasterPassword"),
            hide_input=True
        )
        master_password = Validator.validate_password(master_password)

        if AuthService.login(username, master_password):
            Authorization.__user_auth = True
            click.clear()
            click.secho(t("LoginInterface.Login.SuccessfulAuthorization"), fg="green")
        else:
            click.clear()
            click.secho(t("LoginInterface.Login.FailedAuthorization"), fg="red")

    @staticmethod
    def change_password():
        """Смена пароля."""
        click.secho("Функция в разработке", fg="yellow")

    @staticmethod
    def delete_account():
        """Удаление учетной записи."""
        username = click.prompt("Введите имя вашей учетной записи", type=str)
        username = Validator.validate_username(username)

        master_password = click.prompt("Введите мастер-пароль", hide_input=True)
        master_password = Validator.validate_password(master_password)

        confirmation = click.confirm("Вы уверены, что хотите удалить учетную запись?", default=False)
        if confirmation:
            click.secho("Функция в разработке", fg="yellow")

    @staticmethod
    def change_language():
        """Смена языка интерфейса."""
        lang = click.prompt("Выберите язык (ru/en)", type=click.Choice(["ru", "en"]))
        Language.setup_i18n(lang=lang)
        Language.reload_translations()
        click.secho(t("LoginInterface.ChangeLanguage.ChangeOption"), fg="blue")

    @classmethod
    def get_menu(cls):
        """Возвращает меню с актуальными переводами."""
        return {
            1: t("LoginInterface.LoginMenuOptions.Register"),
            2: t("LoginInterface.LoginMenuOptions.Login"),
            3: t("LoginInterface.LoginMenuOptions.ChangePassword"),
            4: t("LoginInterface.LoginMenuOptions.DeleteAccount"),
            5: t("LoginInterface.LoginMenuOptions.ChangeLanguage"),
            0: t("LoginInterface.LoginMenuOptions.Exit")
        }

    @classmethod
    def login_menu(cls):
        """Главное меню авторизации."""
        while True:
            if Session.is_authenticated():
                return True

            menu = cls.get_menu()
            # Верхняя рамка
            click.secho("=" * 50, fg="blue")
            click.secho(t("LoginInterface.LoginMenu.AuthorizationMenu"), fg="blue", bold=True)
            click.secho("=" * 50, fg="blue")

            # Вывод пунктов меню
            for key, value in menu.items():
                click.echo(f"{click.style(str(key), fg='yellow')} --> {value}")

            # Нижняя рамка
            click.secho("=" * 50, fg="blue")

            choice = click.prompt(t("ChooseOption"), type=int)
            match choice:
                case 1:
                    cls.register()
                case 2:
                    cls.login()
                case 3:
                    cls.change_password()
                case 4:
                    cls.delete_account()
                case 5:
                    cls.change_language()
                case 0:
                    exit(click.style(t("LoginInterface.LoginMenu.Exit"), fg="red"))
                case _:
                    click.secho(t("LoginInterface.LoginMenu.WrongOption"), fg="red")

if __name__ == "__main__":
    Authorization.login_menu()