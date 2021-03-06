# data-full-path

**Цель проекта**: Пройти полный путь от сбора данных до развертывания приложения <br>

**Поставлена задача**: Для нескольких поисковых запросов (тематика: бетон) в яндексе сделать приложение, которое подскажет вероятность попасть на определенную страницу поисковой выдачи в яндексе и покажет рекомендуемые диапазоны значений текстовых характеристик для первой страницы: 
- водность
- спамность
- частота запроса в тексте
- TF-IDF
<br>

Выполненные шаги:  

1.  <a href="/collect">Сбор данных</a>
2.  <a href="/analysis">Анализ и обработка данных</a>
3.  <a href="/prepareToDeploy">Подгтовка модели</a>
4.  <a href="/app">Размещение модели и создание API</a>

**Для каждого поискового запроса**: <br>
Получены рекомендуемый диапазон текстовых характеристик. <br>
Модель решает задачу бинарной классификации (значение метрики ROC_AUC_SCORE варьируется от 68% до 79% для отдельных запросов). Предсказываемые классы: 1) страница будет на первой странице поисковой выдачи; 2) страница будет не на первой странице поисковой выдачи.

### Приложение размещено по адресу https://beton-td-idf.herokuapp.com/
> **Примечание**:<br>
> Приложение размещено на бесплатном тарифе Heroku, поэтому при первом обращении сайт может загружаться около минуты (приложение выходит из спящего режима)

<br>

## Стек технологий

### Сбор данных
API, selenium

### Анализ и обработка данных
pandas, nltk

### Подгтовка модели
sklearn, joblib, pickle

### Размещение модели
Heroku, Flask, API


