# data-full-path

**Цель проекта**: Пройти полный путь от сбора данных до развертывания приложения <br>

**Поставлена задача**: Для нескольких поисковых запросов в яндексе сделать приложение, которое подскажет вероятность попасть на первую страницу поисковой выдачи в яндексе и покажет рекомендуемые диапазон значений текстовых характеристик: 
- водность
- спамность
- частота запроса в тексте
- TF-IDF
<br>

Выполненные шаги:  

1.  <a href="/collect">Сбор данных</a>
2.  <a href="/analysis">Анализ и обработка данных</a>
3.  <a href="/prepareToDeploy">Подгтовка модели</a>
4.  <a href="/app">Размещение модели</a>

<br>

## Стек технологий

### Сбор данных
API, selenium

### Анализ и обработка данных
pandas

### Подгтовка модели
sklearn

### Размещение модели
joblib, Heroku

## https://beton-td-idf.herokuapp.com/
Примечание:<br>
Приложение размещено на бесплатном тарифе Heroku, поэтому при первом обращении сайт может загружаться около минуты (приложение выход из спящего режима)
