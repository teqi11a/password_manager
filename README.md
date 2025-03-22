# Simple Password Manager

**Статус:** *Alpha Release*  
**Важно:** Проект находится на стадии альфа-тестирования. Используйте с осторожностью!

## Описание
Simple Password Manager – это легковесное консольное приложение для безопасного хранения и управления паролями.   
Проект реализован на Python с использованием SQLite для хранения данных, bcrypt для хэширования и cryptography для шифрования.

## Особенности
- Шифрование и безопасное хранение паролей
- Простая и интуитивно понятная CLI-интерфейс (планируется расширение функционала)
- Возможность расширения и модульного развития

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Andrew-s-web/password_manager.git
cd password_manager
```

### Установка зависимостей
***Обратите внимание, что проект использует версию python3.12, версия python на вашем компьютере должна быть не ниже 3.12***  
Все необходимые зависимости перечислены в файле requirements.txt. Для их установки выполните:

```bash
pip install -r requirements.txt
```

Примечание: В настоящее время зависимости устанавливаются напрямую через pip. В скором времени планируется перенос всех зависимостей в requirements.txt, поэтому данная команда станет стандартом установки.

### Инициализация базы данных

Перед первым запуском необходимо создать структуру базы данных. Для этого выполните:

```bash
python db/init_db.py
```

## Запуск программы

### Для запуска основного функционала приложения выполните:

```bash
python main.py
```

## Рекомендации по использованию

 - ### Безопасное хранение данных:
   - Обязательно сделайте резервную копию базы данных и настройте безопасное хранение мастер-пароля.
 - ### Регулярное обновление:
   - Следите за обновлениями проекта и периодически проверяйте наличие новых версий зависимостей. (Пока зависимости не будут перенесены в скрипт автоматической установки)
## Идеи для будущего развития
   - ### Улучшение CLI:
     - Добавление поддержки аргументов командной строки для более гибкого управления (например, через argparse или click).
   - ### Графический интерфейс:
     - Планируется разработка GUI для более удобного взаимодействия с приложением.
   - ### Юнит-тестирование и CI/CD:
     - Написание тестов для основных функций и интеграция с GitHub Actions для автоматической проверки кода.
   - ### Улучшение безопасности:
     - Возможный переход на Argon2 для хэширования, а также расширенная обработка ошибок и логирование.
   - ### Вклад в проект
     - Если у вас есть предложения или вы хотите внести изменения, пожалуйста, создайте ***issue*** или ***pull request***.


***Этот README является предварительной документацией для альфа-версии.  
В будущих релизах планируется расширение функционала и улучшение документации.***