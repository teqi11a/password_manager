import click
from db.storage import PasswordManager, Session
from core.generator import PasswordGenerator
from interfaces.paginate import show_passwords_manual_pagination, show_password_manual_pagination
from translation import Language
from i18n import t

class Choices:
    _min_length = 8
    _max_length = 32
    __interface_borders = {1: "-", 2: "@", 3: "."}
    __passw_interface = {
        1: t("MainInterface.ShowPasswordsOptions.OnePass"),
        2: t("MainInterface.ShowPasswordsOptions.AllPass")
    }

    @classmethod
    def generate_passw_interface(cls):
        """Интерфейс генерации пароля."""
        length = click.prompt(
            t("MainInterface.GeneratePassword.InputPasswordLength"),
            type=int,
            default=16,
            show_default=True
        )
        complexity = click.prompt(
            t("MainInterface.GeneratePassword.InputPasswordComplexity"),
            type=int,
            default=2,
            show_default=True
        )

        try:
            password = PasswordGenerator.generate(length, complexity)
            click.echo(t("MainInterface.GeneratePassword.GeneratedPassword") + click.style(password, fg="green"))

            if click.confirm(t("MainInterface.GeneratePassword.SavePasswordAgreement")):
                service = click.prompt(t("MainInterface.GeneratePassword.ServiceInput"), type=str)
                if PasswordManager.save_password(service, password):
                    click.secho(t("MainInterface.SavePassword.PasswordSaveSuccess"), fg="green")
                else:
                    click.secho(t("MainInterface.SavePassword.PasswordSaveRejected"), fg="red")

        except ValueError as e:
            click.echo(t("MainInterface.GeneratePassword.GenerationFailed") + click.style(str(e), fg="red"))

    @staticmethod
    def save_pass_interface():
        """Интерфейс сохранения пароля."""
        service = click.prompt(t("MainInterface.SavePassword.ServiceInput"), type=str)
        password = click.prompt(t("MainInterface.SavePassword.EnterPassword"), hide_input=True)
        if PasswordManager.save_password(service, password):
            click.secho(t("MainInterface.SavePassword.PasswordSaveSuccess"), fg="green")
        else:
            click.secho(t("MainInterface.SavePassword.PasswordSaveRejected"), fg="red")

    @classmethod
    def show_passw_interface(cls):
        """Интерфейс отображения паролей."""
        click.echo("")
        for key, value in cls.__passw_interface.items():
            click.echo(f"{click.style(str(key), fg='yellow')}: {value}")
        click.echo("")

        user_choice = click.prompt(t("ChooseOption"), type=int)
        match user_choice:
            case 1:
                show_password_manual_pagination()
                click.clear()
            case 2:
                pass_confirm = click.prompt(
                    t("MainInterface.ShowPasswordInterface.ConfirmAction"),
                    hide_input=True
                )
                if PasswordManager.check_password(pass_confirm):
                    click.clear()
                    show_passwords_manual_pagination()
                    click.clear()
                else:
                    click.secho(t("MainInterface.ShowPasswordInterface.WrongMasterPassword"), fg="red")
            case _:
                click.secho(t("MainInterface.ShowPasswordInterface.WrongOption"), fg="red")

class UserInterface:
    __interface_list = {
        1: t("MainInterface.MenuInterface.InterfaceOptions.GeneratePassword"),
        2: t("MainInterface.MenuInterface.InterfaceOptions.ShowPasswords"),
        3: t("MainInterface.MenuInterface.InterfaceOptions.SavePassword"),
        4: t("MainInterface.MenuInterface.InterfaceOptions.ChangeDesign"),
        0: t("MainInterface.MenuInterface.InterfaceOptions.Logout")
    }

    @classmethod
    def menu(cls):
        """Главное меню интерфейса."""
        click.clear()
        while True:
            # Вывод рамки и заголовка
            click.secho("=" * 50, fg="blue")
            click.secho(t("MainInterface.MenuInterface.Title"), fg="blue", bold=True)
            click.secho("=" * 50, fg="blue")

            # Вывод пунктов меню
            for k, v in cls.__interface_list.items():
                click.echo(f"{click.style(str(k), fg='yellow')} --> {v}")

            click.secho("=" * 50, fg="blue")

            # Выбор пользователя
            choice = click.prompt(t("ChooseOption"), type=int)
            match choice:
                case 1:
                    Choices.generate_passw_interface()
                case 2:
                    Choices.show_passw_interface()
                case 3:
                    Choices.save_pass_interface()
                case 4:
                    click.secho(t("MainInterface.MenuInterface.FunctionInDevelopment"), fg="yellow")
                case 0:
                    Session.clear()
                    click.secho(t("MainInterface.MenuInterface.UserLogout"), fg="red")
                    return
                case _:
                    click.secho(t("MainInterface.MenuInterface.WrongOption"), fg="red")

if __name__ == "__main__":
    UserInterface.menu()