#!/bin/bash

# Скрипт развертывания Dronshop в продакшен

set -e

echo " Запуск развертывания Dronshop..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo " Docker не установлен"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo " Docker Compose не установлен"
    exit 1
fi

# Создание .env файла если не существует
if [ ! -f .env ]; then
    echo " Создание .env файла из шаблона..."
    cp .env.production .env
    echo "  Отредактируйте .env файл перед запуском!"
fi

# Остановка существующих контейнеров
echo " Остановка существующих контейнеров..."
docker-compose down

# Сборка и запуск
echo " Сборка и запуск контейнеров..."
docker-compose up -d --build

# Ожидание запуска сервисов
echo " Ожидание запуска сервисов..."
sleep 10

# Проверка статуса
echo " Проверка статуса контейнеров..."
docker-compose ps

echo ""
echo " Развертывание завершено!"
echo ""
echo " Frontend: http://localhost"
echo " Backend API: http://localhost:8000"
echo " База данных: localhost:5432"
echo " Redis: localhost:6379"
echo ""
echo " Для создания администратора выполните:"
echo "   docker-compose exec backend python /app/create_admin.py"
echo ""
echo " Для просмотра логов:"
echo "   docker-compose logs -f"
