# Файлы для размещения

- Файлы размещены на сервисе Heroku,
- Для создания web-приложения используется микрофреймворк Flask


### Точка входа <a href="app.ipynb">app.ipynb</a>

+ Точка входа приложения на Flask
+ Получение данных (URL и поисковый запрос)
+ Вывод информации
+ API: 
  - **/get-list** - запрос на получение списка поисковых запросов (Приммер: https://beton-td-idf.herokuapp.com/get-list)
  - **/analys-page** - запрос на анализ страницы. Передаются два параметра: **quiery_id** - id запроса (из get-list); **url_page** - url страницы для проверки (Пример: https://beton-td-idf.herokuapp.com/analys-page?quiery_id=1&url_page=https%3A%2F%2Fzzbeton.ru%2F). Вернет: **prediction** - вероятность (в процентах) попасть на первую страницу поисковика по заданному запросу; **spamity** - спамность текста; **water_content** - водность текста; **tf_idf** - значение TF-IDF

### Вспомогательные функции <a href="utils.ipynb">utils.ipynb</a>

- Получение списка поисковых запросов

### Обработка данных <a href="convertInput.ipynb">convertInput.ipynb</a>

- Функции обработки входных данных

### Обработка данных <a href="templates">templates</a>

- Папка с шаблонами html-страниц для приложения

<hr>


<hr>
<a href='../prepareToDeploy'>Назад - Подготовка к размещению</a> <br>
