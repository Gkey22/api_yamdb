# api_yamdb
Описание
Проект YaMDb собирает отзывы пользователей на произведения


##
Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Gkey22/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
``` 
pip install -r requirements.txt
```

Выполнить миграции:
``` 
python manage.py migrate
``` 

Загрузить тестовые данные:
``` 
python manage.py load_csv
``` 

Запустить проект:
``` 
python manage.py runserver
``` 

Документация в формате Redoc:
``` 
http://127.0.0.1:8000/redoc/
``` 

##
Авторы:
Гриценко vkontaktensk@yandex.ru
Евсюков Bornki11@yandex.ru
Sunduyool ssedu.s@yandex.ru
