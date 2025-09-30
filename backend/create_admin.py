#!/usr/bin/env python3
"""
Скрипт для создания администратора в продакшен окружении
"""

import sys
import os

# Добавляем путь к бэкенду для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role

def create_admin_user():
    """Создает пользователя с ролью администратора"""
    
    print("Создание администратора...")
    
    try:
        db = SessionLocal()
        
        # Создание роли администратора если не существует
        admin_role = db.query(Role).filter(Role.name == 'admin').first()
        if not admin_role:
            print("Создание роли 'admin'...")
            admin_role = Role(name='admin')
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("Роль 'admin' создана")
        else:
            print("Роль 'admin' уже существует")
        
        # Запрос данных администратора
        print("\nВведите данные администратора:")
        phone = input("Телефон (например, +79991234567): ").strip()
        name = input("Имя: ").strip()
        email = input("Email (опционально): ").strip() or None
        
        # Проверка существования пользователя
        existing_user = db.query(User).filter(User.phone == phone).first()
        if existing_user:
            print(f"Пользователь с телефоном {phone} уже существует")
            if input("Сделать его администратором? (y/n): ").lower() == 'y':
                if admin_role not in existing_user.roles_rel:
                    existing_user.roles_rel.append(admin_role)
                    db.commit()
                    print(f"Пользователь {phone} назначен администратором")
                else:
                    print("Пользователь уже является администратором")
            return
        
        # Создание нового администратора
        admin_user = User(
            phone=phone,
            name=name,
            email=email,
            is_verified=True
        )
        admin_user.roles_rel = [admin_role]
        db.add(admin_user)
        db.commit()
        
        print(f"\n✅ Администратор успешно создан!")
        print(f"📱 Телефон: {phone}")
        print(f"👤 Имя: {name}")
        if email:
            print(f"📧 Email: {email}")
        print(f"🔑 Роль: администратор")
        
    except Exception as e:
        print(f"❌ Ошибка при создании администратора: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
