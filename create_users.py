import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maint_system.settings')
django.setup()

from accounts.models import User

# Создаём тестовых пользователей с паролями
users_data = [
    ('admin_otir', 'admin123', 'admin', 'Управление ОТК', '+79001112200'),
    ('eng_ivanov', 'engineer123', 'engineer', 'Механика', '+79001112201'),
    ('eng_petrov', 'engineer123', 'engineer', 'Электрика', '+79001112202'),
    ('tech_sidorov', 'tech123', 'technician', 'Цех 1', '+79001112203'),
    ('tech_kuznetsov', 'tech123', 'technician', 'Цех 2', '+79001112204'),
    ('tech_popov', 'tech123', 'technician', 'Цех 1', '+79001112205'),
    ('store_morozov', 'store123', 'storekeeper', 'Склад A', '+79001112212'),
    ('store_novikov', 'store123', 'storekeeper', 'Склад B', '+79001112213'),
    ('trainee_smirnov', 'trainee123', 'trainee', 'Практика', '+79001112215'),
    ('trainee_fedorov', 'trainee123', 'trainee', 'Практика', '+79001112216'),
]

for username, password, role, department, phone in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'role': role,
            'department': department,
            'phone': phone,
            'is_active': True,
        }
    )
    if created:
        user.set_password(password)
        user.save()
        print(f'✅ Создан пользователь: {username} ({role})')
    else:
        print(f'⚠️ Пользователь {username} уже существует')

print('\n🎉 Готово! Все пользователи созданы.')
