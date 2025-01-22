# Backend Change Logger

## Описание проекта

**Backend Change Logger** — это инструмент для автоматического сбора изменений из репозиториев и ведения логов изменений. Он анализирует коммиты, извлекает информацию о модификациях в коде и записывает их в файлы логов.

### Основные функции:

- Автоматический сбор изменений из Git-репозиториев
- Создание и обновление файлов логов
- Поддержка нескольких проектов и сервисов
- Гибкая настройка через конфигурационные файлы

## Установка и настройка

### Требования

- Python 3.10+
- Poetry (для управления зависимостями)
- Доступ к Git-репозиториям

# Запуск проекта

1. Установка Poetry с помощью pip:
   ```bash
   pip install poetry
   ```
2. Запустить виртуальное окружение
   ```bash
   poetry shell
   ```
3. Установить зависимости
   ```bash
   poetry install
   ```
4. Задать настройки в переменых окружения:  
   Пример для MacOS и Linux:

   ```
   export DYNACONF_GIT_LOGIN=<логин к репозиторию от куда забираем информацию>
   export DYNACONF_GIT_PASSWORD=<пароль к репозиторию от куда забираем информацию>
   export DYNACONF_GIT_LOGIN_CHANGELOGS=<логин к репозиторию куда надо пушить changelogs>
   export DYNACONF_GIT_PASSWORD_CHANGELOGS=<пароль к репозиторию куда надо пушить changelogs>
   export DYNACONF_REPO_URL=<url репозитория>
   export DYNACONF_SRC_FOLDER=<папка репозитория в дял которой выполняем скрипт>
   export DYNACONF_SAVE_RESULT_IN_REPO=<параметр для сохранения change_logs на удаленный репозиторий. True если надо сохранять. False если не надо. По умолчанию False>
   export DYNACONF_REPO_URL_FOR_CHANGELOGS=<url репозитория куда надо пушить changelogs>
   export DYNACONF_SRC_FOLDER_FOR_CHANGELOGS=<папка на удаленном репозитории куда будут сохраняться changelogs. По умолчанию changelogs.>
   export DYNACONF_LAST_COMMIT_HASH=<хэш коммита с которого надо начинать формировать git log. По умолчанию все коммиты беруться>
   export DYNACONF_LOCAL_REPO_PATH=<абсолютный путь к вашему локальному репозиторию. Если если переменная не задана,  то скрипт работает с удаленным репозиторием.>
   ```

   Пример для Windows:

   ```
   setx DYNACONF_GIT_LOGIN "<логин к репозиторию от куда забираем информацию>"
   setx DYNACONF_GIT_PASSWORD "<пароль к репозиторию от куда забираем информацию>"
   setx DYNACONF_GIT_LOGIN_CHANGELOGS "<логин к репозиторию куда надо пушить changelogs>"
   setx DYNACONF_GIT_PASSWORD_CHANGELOGS "<пароль к репозиторию куда надо пушить changelogs>"
   setx DYNACONF_REPO_URL "<url репозитория>"
   setx DYNACONF_SRC_FOLDER "<папка репозитория в дял которой выполняем скрипт>"
   setx DYNACONF_SAVE_RESULT_IN_REPO "<параметр для сохранения change_logs на удаленный репозиторий. True если надо сохранять. False если не надо. По умолчанию False>"
   setx DYNACONF_REPO_URL_FOR_CHANGELOGS "<url репозитория куда надо пушить changelogs>"
   setx DYNACONF_SRC_FOLDER_FOR_CHANGELOGS "<папка на удаленном репозитории куда будут сохраняться changelogs. По умолчанию changelogs.>"
   setx DYNACONF_LAST_COMMIT_HASH "<хэш коммита с которого надо начинать формировать git log. По умолчанию все коммиты беруться>"
   setx DYNACONF_LOCAL_REPO_PATH "<абсолютный путь к вашему локальному репозиторию. Если если переменная не задана,  то скрипт работает с удаленным репозиторием.>"
   ```

   Или задать настройки можно в settings.toml:

   ```
   [default]
   REPO_URL = "https://git.effectivetrade.ru/EFTR/EFTR2.git"
   SRC_FOLDER = "tools/"
   LOCAL_REPO_PATH = ""
   REPO_URL_FOR_CHANGELOGS = ""
   SRC_FOLDER_FOR_CHANGELOGS = ""
   LAST_COMMIT_HASH = ""
   SAVE_RESULTS_IN_REPO = "False"
   ```

   Данные авторизации для репозитория также можно задать в файле .env:

   ```
   DYNACONF_GIT_LOGIN=<логин к репозиторию от куда забираем информацию>
   DYNACONF_GIT_PASSWORD=<пароль к репозиторию от куда забираем информацию>
   DYNACONF_GIT_LOGIN_CHANGELOGS=<логин к репозиторию куда надо пушить changelogs>
   DYNACONF_GIT_PASSWORD_CHANGELOGS=<пароль к репозиторию куда надо пушить changelogs>
   ```

   Переменные окружения, заданные через export или setx, имеют приоритет над значениями, определенными в файлах конфигурации.

5. Запустить скрипт get_commits.py:
   ```bash
   python get_commits.py
   ```

В корне проекта создастся папка `changelogs` в которой будут все коммиты.
