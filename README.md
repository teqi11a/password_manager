# Simple Password Manager
## Установка и инициализация базы данных

Чтобы начать работу с вашим проектом, выполните следующие шаги для создания базы данных:

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш_логин/password_manager.git
cd password_manager
```
### 2. Установите необходимые проекту зависимости
Убедитесь, что у вас установлены все необходимые зависимости, такие как bcrypt и sqlite3. Вы можете установить их с помощью pip:
``` bash
pip install bcrypt
pip install sqlite3
pip install cryptography
```
### 3. Инициализируйте базу данны
Запустите скрипт init_db.py, чтобы создать структуру базы данн
``` bash
python init_db.py
```
## Запуск основной программы
Теперь вы готовы к запуску программы через файл main.py
``` bash
python main.py
```
