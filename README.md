# Приложение Shorty URL
* Приложение Shorty URL умеет сокращать ссылки до 10 символов после доменного имени. 
* Ссылки хранятся в базе данных PostgresQL
* В админ-панели Django можно управлять ссылками.
## Запуск приложения
1. Создайте рабочую директорию для хранения проекта:
<br> `mkdir ~/Dev`
2. Склонируйте репозиторий на ваш компьютер:
<br> `https://github.com/Talpik/shortly_url.git ~/Dev/shorty_url`
3. Установите Docker для запуска приложения:
<br> <https://docs.docker.com/engine/install/>
4. Перейдите в папку проекта **shorty_url**:
<br> `cd ~/Dev/shorty_url`
5. Запустите утилиту **docker-compose**, чтобы развернуть контейнеры:
<br> `docker-compose up -d --build`
6. Проверьте запущенные контейнеры:
<br> `docker container ls` и скопируйте занчение **CONTAINER ID** контейнера **web**
7. Проведите миграции внутри контейнера **web**:
<br> `docker exec -it <container id> python manage.py migrate`
8. Создайте суперпользователя:
<br> `docker exec -it <container id> python manage.py createsuperuser`
9. Соберите статику в внутри контейнера в `/code/static`:
<br> `docker exec -it <container id> python manage.py collectstatic`
## Настройка доступных хостов
Настройка доступных хостов осуществляется в файле *.env*:
<br> `ALLOWED_HOSTS=127.0.0.1,localhost`
<br> Через запятую можно добавлять другие значения.
## Основные точки доступа
1. Админка:          <br>`127.0.0.1/admin/`
2. API сокращения ссылок:         <br>`127.0.0.1/graphql`
3. Переход по ссылке: <br>`127.0.0.1/<hash_sum>`
## Создание ссылки
1. Перейдите по адресу `127.0.0.1/graphql`
2. Выполните первое сокращение ссылки, запустив следующее выражение в левой части экрана:
```
mutation {
   createUrl(fullUrl:"https://www.yandex.ru") {
    url {
      id
      fullUrl
      urlHash
      clicks
      createdAt
    }
  }
}
```
Создана ссылка с именем `createURL` и аргументом `fullUrl`
3. Приложение покажет слудующий вывод:
```
{
  "data": {
    "createUrl": {
      "url": {
        "id": "1",
        "fullUrl": "https://www.yandex.com",
        "urlHash": "f845599b09",
        "clicks": 0,
        "createdAt": "2021-05-21T19:15:10.820062+00:00"
      }
    }
  }
}
```
4. Получить список всех ссылок:
```
query {
  urls {
    id
    fullUrl
    urlHash
    clicks
    createdAt
  }
}
```
5. Фильтрация:
```
query {
  urls(url:"yandex") {
    id
    fullUrl
    urlHash
    clicks
    createdAt
  }
}
```
6. Пагинация (показать первые 2 записи - пропустив одну запись):
```
query {
  urls(first: 2, skip: 1) {
    id
    fullUrl
    urlHash
    clicks
    createdAt
  }
}
```
