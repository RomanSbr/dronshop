

## Технологии

- **Backend**: Python + FastAPI
- **Frontend**: Vue.js 3 + Vite
- **База данных**: PostgreSQL
- **Кэш**: Redis
- **Веб-сервер**: Nginx
- **Контейнеризация**: Docker + Docker Compose

## Быстрый старт

### Требования

- Docker 20.10+
- Docker Compose 2.0+

### Запуск в продакшене

2. **Настройте переменные окружения**
   ```bash
   cp .env.production .env
   # Отредактируйте .env файл с вашими настройками
   ```

3. **Запустите приложение**
   ```bash
   docker-compose up -d
   ```

4. **Приложение будет доступно по адресу**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## Структура проекта

```
dronshop/
├── backend/              # FastAPI бэкенд
│   ├── src/app/         # Исходный код приложения
│   ├── requirements.txt # Зависимости Python
│   └── Dockerfile       # Docker образ бэкенда
├── frontend/            # Vue.js фронтенд
│   ├── src/            # Исходный код фронтенда
│   ├── package.json    # Зависимости Node.js
│   ├── Dockerfile      # Docker образ фронтенда
│   └── nginx.conf      # Конфигурация Nginx
├── docker-compose.yml  # Docker Compose конфигурация
└── README.md          # Документация
```

## Административная панель

Административная панель доступна по адресу `/admin` после входа под учетной записью с ролью `admin`.

### Функционал админ-панели:

- **Управление товарами** - добавление, редактирование, удаление товаров
- **Управление категориями** - создание иерархии категорий
- **Управление запасами** - контроль остатков на складе
- **Управление заказами** - просмотр и обработка заказов
- **Управление пользователями** - блокировка, назначение ролей
- **Управление отзывами** - модерация отзывов
- **Настройки сайта** - основные настройки магазина

## Переменные окружения

Основные переменные окружения для настройки:

- `SECRET_KEY` - секретный ключ для JWT токенов
- `DATABASE_URL` - URL подключения к PostgreSQL
- `REDIS_URL` - URL подключения к Redis
- `ALLOWED_ORIGINS` - разрешенные домены для CORS
- `DEV_LOGIN_ENABLED` - отключить для продакшена (false)
- `DEV_SEED` - отключить сидирование данных (false)

## Администрирование

### Создание администратора

Для создания администратора выполните:

```bash
docker-compose exec backend python -c "
from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role

db = SessionLocal()

# Создание роли администратора если не существует
admin_role = db.query(Role).filter(Role.name == 'admin').first()
if not admin_role:
    admin_role = Role(name='admin')
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)

# Создание пользователя администратора
admin_user = User(
    phone='+79991234567',
    name='Администратор',
    email='admin@example.com',
    is_verified=True
)
admin_user.roles_rel = [admin_role]
db.add(admin_user)
db.commit()

print('Администратор создан:', admin_user.phone)
"
```

### Резервное копирование базы данных

```bash
docker-compose exec postgres pg_dump -U dronshop dronshop > backup.sql
```

### Восстановление из резервной копии

```bash
docker-compose exec -T postgres psql -U dronshop dronshop < backup.sql
```

## Мониторинг и логи

### Просмотр логов

```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

### Мониторинг состояния

```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

## Обновление приложения

1. Остановите текущую версию:
   ```bash
   docker-compose down
   ```

2. Обновите код:
   ```bash
   git pull origin main
   ```

3. Пересоберите и запустите:
   ```bash
   docker-compose up -d --build
   ```

## Безопасность

### Рекомендации по безопасности

1. **Измените секретный ключ** в `.env` файле
2. **Измените пароли БД** от стандартных значений
3. **Настройте SSL/TLS** для production окружения
4. **Ограничьте доступ** к административной панели
5. **Регулярно обновляйте** зависимости и образы Docker

### Безопасность в Docker

- Все сервисы запускаются с минимальными привилегиями
- Используются отдельные пользователи для каждого сервиса
- Данные сохраняются в volumes для изоляции
- Сеть настроена для минимального доступа между сервисами

## Лицензия

MIT License - см. файл LICENSE для подробностей.
