## 🚀 Быстрый старт (Windows / PowerShell) 2

⚙️ Доступ к приложению
Главная страница: 127.0.0.1
Админ-панель: 127.0.0.1
Логин: Admin
Пароль: KorokNET
🛠 Технологии
Backend: Python 3.12, Django 4.2.27
Frontend: JS, Bootstrap
Database: SQLite
Environment: PowerShell (Windows)

```powershell
# 1. Клонирование репозитория
cd ~/Desktop
git clone https://github.com/cambodia69691-collab/-.git
cd -
code . -r

# 2. Создание и активация виртуального окружения
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

# 3. Установка зависимостей и подготовка БД
pip install -r requirements.txt
python manage.py migrate

# 4. Автоматическое создание суперпользователя (Admin / KorokNET)
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); username='Admin'; password='KorokNET'; email='admin@example.com'; u, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); u.set_password(password); u.is_staff=True; u.is_superuser=True; u.email=email; u.save(); print('Superuser created' if created else 'Superuser updated')"

# 5. Запуск сервера разработки
python manage.py runserver


# . Все команды одним блоком

cd ~/Desktop
git clone https://github.com/cambodia69691-collab/-.git
cd -
code . -r
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); username='Admin'; password='KorokNET'; email='admin@example.com'; u, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); u.set_password(password); u.is_staff=True; u.is_superuser=True; u.email=email; u.save(); print('Superuser created' if created else 'Superuser updated')"
python manage.py runserver
