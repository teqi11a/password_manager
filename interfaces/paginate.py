import click

from i18n import t
from tabulate import tabulate
from db.storage import PasswordManager


def show_passwords_manual_pagination():
    """Ручная пагинация для вывода таблицы с паролями."""
    data = PasswordManager.get_all_passwords()
    if not data:
        click.echo(click.style("Нет сохранённых паролей.", fg="yellow"))
        return

    page_size = 5  # Количество строк на странице
    current_page = 0

    while True:
        click.clear()

        start = current_page * page_size
        end = start + page_size
        page_data = data[start:end]

        headers = [click.style("ID", fg="blue"), click.style("Сервис", fg="blue"), click.style("Пароль", fg="blue")]
        rows = [
            [click.style(str(pwd_id), fg="yellow"), click.style(service, fg="green"), click.style(password, fg="red")]
            for pwd_id, service, password in page_data
        ]
        table = tabulate(rows, headers=headers, tablefmt="fancy_grid")
        click.echo(table)

        # Подсказка для пользователя
        click.echo(click.style(f"Страница {current_page + 1}", fg="blue"))
        click.echo(click.style("n - следующая страница, p - предыдущая страница, q - выход", fg="yellow"))

        # Обработка ввода пользователя
        action = click.prompt("Выберите действие", type=str, default="q")
        if action == "n" and end < len(data):
            current_page += 1
        elif action == "p" and current_page > 0:
            current_page -= 1
        elif action == "q":
            break

def show_password_manual_pagination():
    """Ручная пагинация для вывода таблицы с паролями."""
    service = click.prompt(t("MainInterface.ShowPasswordInterface.ServiceName"), type=str)
    data = PasswordManager.get_password(service)
    if not data:
        click.echo(click.style("Нет сохранённых паролей.", fg="yellow"))
        return

    page_size = 5
    current_page = 0

    while True:
        click.clear()

        start = current_page * page_size
        end = start + page_size
        page_data = data[start:end]

        headers = [click.style("Сервис", fg="blue"), click.style("Пароль", fg="blue")]
        rows = [
            [click.style(service_name, fg="green"), click.style(password, fg="red")]
            for service_name, password in page_data
        ]
        table = tabulate(rows, headers=headers, tablefmt="fancy_grid")

        click.echo(table)

        # Подсказка для пользователя
        click.echo(click.style(f"Страница {current_page + 1}", fg="blue"))
        click.echo(click.style("n - следующая страница, p - предыдущая страница, q - выход", fg="yellow"))

        # Обработка ввода пользователя
        action = click.prompt("Выберите действие", type=str, default="q")
        if action == "n" and end < len(data):
            current_page += 1
        elif action == "p" and current_page > 0:
            current_page -= 1
        elif action == "q":
            break