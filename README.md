### Для запуска установите django:
```
pip install django
```
### Также virtual env и некоторые зависимости проекта:
```
pip install virtualenv
python -m pip install Pillow
```
### При запуске проекта следуйте инструкции:
```
cd recommends
cd env
.\scripts\activate
cd ..
```
### Сделайте миграции для создания базы данных:
```
python manage.py makemigrations
python manage.py migrate 
```
### Создайте суперпользователя для взаимодействия админ-панелью:
```
python manage.py createsuperuser
```
# ЗАПУСКАЙТЕ ПРОЕКТ:
```
python manage.py runserver
```