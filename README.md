# REST-API

## Суть проекта:

Необходимость в разработке сервиса терминологии и REST-API к нему.

## Стек:

1. База данных: **PostgreSQL**.

2. Фреймворк: **Django-rest-framework**.

3. WSGI: **Gunicorn**.

4. Веб-сервер: **Nginx**.

5. Развертывание: **Docker-Compose**. 

## Пример работы API:

### Получение списка справочников / справочников, актуальных на указанную дату:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API/Komtek_handbook.gif)

### Получение списка элементов справочников / элеметов заданного справочника текущей версии / элементов заданного справочника указанной версии:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API/Komtek_itemhandbook.gif)

### Валидация элементов заданного справочника текущей версии:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API/Komtek_itemhandbookvalidator_many.gif)

### Валидация элемента заданного справочника по указанной версии:

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API/Komtek_itemhandbookvalidator_many.gif)

## Административное управление сервисом:

Сервис предоставляет удобную административную панель, в которой совершать различные манипуляции со справочниками и их элементами. 

![alt](https://github.com/coldcloudgold/illustration/blob/main/Project/DRF_API/Komtek_admin.gif)

## Запуск проекта:

Изменить название *example.env* на *.env*, при необходимости внеся в него коррективы (для *Prod* оставить **DJANGO_DEBUG** пустым, для *Dev* - поставить любое значение).

*Prod*:

1. Убедиться, что необходимые порты для работы проекта не заняты (8080 - nginx, 5433 - postgres, 8001 - django/gunicorn): 

`sudo netstat -tulpn | grep :<xxxx>`

где `xxxx` - номер порта.

2. Если на данных портах запущены стандартные сервисы, их необходимо выключить: 

```sudo kill `sudo lsof -t i:<xxxx>` ```

3. Создать docker-compose: 

`docker-compose build`

4. Запустить docker-compose: 

`mkdir static; docker-compose up -d`

5. Остановить и удалить docker-compose:

`docker-compose down -v`

*Dev*:

1. Убедиться, что необходимые порты для работы проекта не заняты (8080 - django/gunicorn): 

`sudo netstat -tulpn | grep :<xxxx>`

где `xxxx` - номер порта.

2. Если на данных портах запущены стандартные сервисы, их необходимо выключить: 

```sudo kill `sudo lsof -t i:<xxxx>` ```

3. Запустить скрипт:

`./dev_entrypoint.sh`

4. Остановить работу:

`Ctrl+C`

## Эндпоинты и методы:

**Эндпоинты**:
```
/api/handbook/<pk>
/api/item_handbook/<pk>
/api/item_handbook_validator/
```

**Методы**:

*GET*

Ссылка | Значение
--- | ---
/api/handbook/ | Получение списка справочников
/api/handbook/?validity_date=2021/07/15 | Получение списка справочников, актуальных на указанную дату
/api/item_handbook/ | Получение элементов справочников
/api/item_handbook/?global_id=1 | Получение элементов заданного справочника текущей версии
/api/item_handbook/?global_id=1&version=0.0.1 | Получение элементов заданного справочника указанной версии


*POST*

Ссылка | Значение
--- | --- 
/api/item_handbook_validator/ | Валидация элементов заданного справочника текущей версии `*`
/api/item_handbook_validator/ | Валидация элемента заданного справочника по указанной версии `**`

`*` - Пример тела запроса:
```
[
    {
        "global_id": 1
    },
    {
        "code": "Test item 1",
        "value": "1"
    },
    {
        "code": "Test item 2",
        "value": "2"
    },
]
```

`**` - Пример тела запроса:
```
[
    {
        "global_id": 1,
        "version" "0.0.1"
    },
    {
        "code": "Test item 1",
        "value": "1"
    },
    {
        "code": "Test item 2",
        "value": "2"
    },
]
```

## Полезное:

### Зайти в панель администратора (пользователь создается по умолчанию, доступ для входа - /admin/), если не менялись соответствующие параметры в окружении:

```
Name: name_admin
Email: email_admin@admin.admin
Password: password_admin
```

### Запустить тесты:

`./manage.py test`
