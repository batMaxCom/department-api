# DepartmentAPI

Управление иерархической структурой отделов и сотрудников. REST API на **FastAPI** с архитектурой **Clean Architecture / DDD**, CQRS через медиатор и **PostgreSQL** в качестве хранилища.

---

## Архитектура

Проект разделён на классические слои **Clean Architecture**:

```
domain/         — Сущности, Value Objects, интерфейсы репозиториев
application/    — Use Cases (команды, запросы, обработчики), DTO, порты (CQRS, генератор ID, транзакции)
infrastructure/ — Реализации: SQLAlchemy, Snowflake ID, Mediator, Alembic
presentation/   — FastAPI-контроллеры, CLI (Click), схемы ответов, обработчики ошибок
entrypoint/     — DI-контейнеры (Dishka), фабрика приложения, точка входа
```

### CQRS через Mediator

Команды и запросы отправляются через `Sender`, который через `MediatorImpl` находит зарегистрированный `Handler` в `Registry` и вызывает его, разрешая зависимости из DI-контейнера.

- `CreateDepartmentCommand`, `UpdateDepartmentCommand`, `DeleteDepartmentCommand`, `CreateEmployeeCommand`
- `GetDepartmentQuery`

---

## API Endpoints

| Метод    | Путь                              | Описание                                                         |
|----------|-----------------------------------|------------------------------------------------------------------|
| `GET`    | `/healthcheck`                    | Проверка доступности сервиса                                     |
| `POST`   | `/api/departments`                | Создать отдел                                                    |
| `GET`    | `/api/departments/{id}`           | Получить дерево отделов (с опциями `depth`, `include_employees`) |
| `PATCH`  | `/api/departments/{id}`           | Обновить отдел (название, родитель)                              |
| `DELETE` | `/api/departments/{id}`           | Удалить отдел (cascade / reassign)                               |
| `POST`   | `/api/departments/{id}/employees` | Создать сотрудника в отделе                                      |

Swagger-документация доступна по пути `/docs`.

### Примечание к методам удаления:
1. cascade

Рекурсивно удаляет выбранное подразделение вместе со всеми его дочерними подразделениями и всеми сотрудниками во всей подветке.

2. reassign

Удаляет только выбранное подразделение.
Сотрудники удаляемого подразделения переводятся в `reassign_to_department_id`.
Дочерние подразделения перепривязываются к родительскому подразделению удаляемого узла.

Ограничения:
- Нельзя выполнить reassign без указания reassign_to_department_id
- Нельзя переназначить сотрудников или переместить подразделение в самого себя
- Нельзя выбирать reassign_to_department_id, находящийся в поддереве удаляемого подразделения
---

## Технологии

- **Python 3.12+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** (imperative mapping) — ORM
- **PostgreSQL 17** — база данных
- **Alembic** — миграции
- **Dishka** — DI-контейнер
- **Click** — CLI
- **Snowflake ID** — генератор идентификаторов
- **uv** — менеджер зависимостей
- **mypy** (strict) — статическая типизация
- **ruff** — линтер

---

## Быстрый старт

### Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL 17 (или Docker)

### Локальная разработка
После поднятие БД:
```bash
# Клонировать репозиторий
git clone <url>
cd DepartmentAPI

# Скопировать конфигурацию
cp env.template .env

# Установить зависимости
uv sync

# Применить миграции
uv run department-cli migrate

# Запустить сервер
uv run department-cli start-uvicorn
```

Сервер будет доступен на `http://localhost:8000` или на порту указанном в `.env`.

### Через Docker Compose

```bash
docker compose up
```

Поднимаются два контейнера: API и PostgreSQL.

---

## CLI

```bash
department-cli migrate                   # Применить миграции
department-cli make-migrations -m "msg"  # Создать новую миграцию
department-cli rollback                  # Откатить последнюю миграцию
department-cli start-uvicorn             # Запустить FastAPI-сервер
```

Либо напрямую:

```bash
python -m department.entrypoint.web
```

---

## Конфигурация

Все настройки задаются через переменные окружения (см. `env.template`):

| Переменная          | По умолчанию | Описание                   |
|---------------------|--------------|----------------------------|
| `POSTGRES_HOST`     | `localhost`  | Хост БД                    |
| `POSTGRES_PORT`     | `5432`       | Порт БД                    |
| `POSTGRES_USER`     | `postgres`   | Пользователь БД            |
| `POSTGRES_PASSWORD` | `postgres`   | Пароль БД                  |
| `POSTGRES_DATABASE` | `postgres`   | Название БД                |
| `SERVER_HOST`       | `127.0.0.1`  | Хост сервера               |
| `SERVER_PORT`       | `8000`       | Порт сервера               |
| `CORS_ORIGINS`      | `*`          | Разрешённые CORS-источники |
| `DEBUG`             | `False`      | Режим отладки              |
| `MACHINE_ID`        | `1`          | ID машины для Snowflake ID |

---

## Миграции

После изменения моделей базы данных:

```bash
department-cli make-migrations -m "описание изменений"
department-cli migrate
```

---