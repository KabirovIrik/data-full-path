import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from bs4 import BeautifulSoup
import joblib, pickle, re, nltk, csv, pymorphy2, requests
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import label_binarize
from selenium import webdriver
#from nltk.corpus import stopwords as nltk_stopwords


lr = 172
tokenizer = RegexpTokenizer(r'\w+')
morph = pymorphy2.MorphAnalyzer()
replace_city_name = 'название_город' # название для замены
USE_SELENIUM = False

#stopwords = set(nltk_stopwords.words('russian'))
#my_stopwrods = ['а', 'будем', 'будет', 'будете', 'будешь', 'буду', 'будут', 'будучи', 'будь', 'будьте', 'бы', 'был', 'была', 'были', 'было', 'быть', 'в', 'вам', 'вами', 'вас', 'весь', 'во', 'вот', 'все', 'всё', 'всего', 'всей', 'всем', 'всём', 'всеми', 'всему', 'всех', 'всею', 'всея', 'всю', 'вся', 'вы', 'да', 'для', 'до', 'его', 'едим', 'едят', 'ее', 'её', 'ей', 'ел', 'ела', 'ем', 'ему', 'емъ', 'если', 'ест', 'есть', 'ешь', 'еще', 'ещё', 'ею', 'же', 'за', 'и', 'из', 'или', 'им', 'ими', 'имъ', 'их', 'к', 'как', 'кем', 'ко', 'когда', 'кого', 'ком', 'кому', 'комья', 'которая', 'которого', 'которое', 'которой', 'котором', 'которому', 'которою', 'которую', 'которые', 'который', 'которым', 'которыми', 'которых', 'кто', 'меня', 'мне', 'мной', 'мною', 'мог', 'моги', 'могите', 'могла', 'могли', 'могло', 'могу', 'могут', 'мое', 'моё', 'моего', 'моей', 'моем', 'моём', 'моему', 'моею', 'можем', 'может', 'можете', 'можешь', 'мои', 'мой', 'моим', 'моими', 'моих', 'мочь', 'мою', 'моя', 'мы', 'на', 'нам', 'нами', 'нас', 'наса', 'наш', 'наша', 'наше', 'нашего', 'нашей', 'нашем', 'нашему', 'нашею', 'наши', 'нашим', 'нашими', 'наших', 'нашу', 'не', 'него', 'нее', 'неё', 'ней', 'нем', 'нём', 'нему', 'нет', 'нею', 'ним', 'ними', 'них', 'но', 'о', 'об', 'один', 'одна', 'одни', 'одним', 'одними', 'одних', 'одно', 'одного', 'одной', 'одном', 'одному', 'одною', 'одну', 'он', 'она', 'оне', 'они', 'оно', 'от', 'по', 'при', 'с', 'сам', 'сама', 'сами', 'самим', 'самими', 'самих', 'само', 'самого', 'самом', 'самому', 'саму', 'свое', 'своё', 'своего', 'своей', 'своем', 'своём', 'своему', 'своею', 'свои', 'свой', 'своим', 'своими', 'своих', 'свою', 'своя', 'себе', 'себя', 'собой', 'собою', 'та', 'так', 'такая', 'такие', 'таким', 'такими', 'таких', 'такого', 'такое', 'такой', 'таком', 'такому', 'такою', 'такую', 'те', 'тебе', 'тебя', 'тем', 'теми', 'тех', 'то', 'тобой', 'тобою', 'того', 'той', 'только', 'том', 'томах', 'тому', 'тот', 'тою', 'ту', 'ты', 'у', 'уже', 'чего', 'чем', 'чём', 'чему', 'что', 'чтобы', 'эта', 'эти', 'этим', 'этими', 'этих', 'это', 'этого', 'этой', 'этом', 'этому', 'этот', 'этою', 'эту', 'я']
#all_stopwords = set(my_stopwrods).union(stopwords)

all_stopwords = []
with open('stopwords.csv', encoding='utf-8') as csv_file:
    file = csv.reader(csv_file, delimiter=';')
    for row in file:
        all_stopwords.append(row[0])

# Входные данные:
# - html-текст
# - Поисковый запрос
# - Город

# In[3]:


if USE_SELENIUM:
    chromedriver = 'd:/games/chrome/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('headless')  # для открытия headless-браузера
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)




# In[5]:


df_cities = pd.read_csv('lr_regions.csv', encoding='UTF-8', sep=';')
df_lr = df_cities[df_cities['lr'] == str(lr)]
city_name = df_lr['name1'].values[0]
all_cities = df_lr['name2'].to_list() + df_lr['name1'].to_list() # список городов в Им.падеже в конце
with open('qu_idf.pkl', 'rb') as f:
    qu_idf = pickle.load(f)


# # Готовим текст

# In[6]:


def replaceCityName(val):
    for city in all_cities:
        val = val.lower().replace(city.lower(), replace_city_name)
    return val

def getTextContent(val):
    soup = BeautifulSoup(val, 'lxml')
    return soup.body.get_text(separator=" ", strip=True)

def get_lemm(text):
    """
    Подготив строки, токенизируем и проведем лемматизацию
    """
    word_list = nltk.word_tokenize(text)
    return ' '.join([morph.parse(w)[0].normal_form for w in word_list])




# # Получаем фичи

# In[7]:


#len_mt, len_md, len_kw, len_w_mt, len_w_md, len_w_kw
def getMeta(val):
    """
    val - html docuemnt
    """
    soup = BeautifulSoup(val, 'lxml')
    try:
        word_list = nltk.word_tokenize(soup.head.title.text.replace('\xa0', ' '))
        title = ' '.join([morph.parse(w)[0].normal_form for w in word_list])
    except:
        title = ''
        
    try:
        word_list = nltk.word_tokenize(soup.head.find_all(attrs={"name" : "description"})[0]['content'].replace('\xa0', ' '))
        descr = ' '.join([morph.parse(w)[0].normal_form for w in word_list])
    except:
        descr = ''
    try:
        word_list = nltk.word_tokenize(soup.head.find_all(attrs={"name" : "keywords"})[0]['content'].replace('\xa0', ' '))
        kw = ' '.join([morph.parse(w)[0].normal_form for w in word_list])
    except:
        kw = ''
    return title.lower(), descr.lower(), kw.lower(), len(title), len(descr), len(kw)

def getLenWords(val):
    return len(val.split(' '))

def getLenKeyWords(val):
    cnt_semi = val.count(',')
    return cnt_semi + ((cnt_semi > 0) * 1) or (len(val) > 0) * 1

# words_count, words_count_sw
def getWordsCount(text):
    word_list = tokenizer.tokenize(text) # с стоп-словами
    word_list_sw = [w for w in word_list if not w in all_stopwords] # без стоп-слов
    return len(word_list), len(word_list_sw)

# spamity, max_spam
def getSpamity(val):
    # получаем список слов и исключаем стоп слова
    word_list = [w for w in tokenizer.tokenize(val) if not w in all_stopwords] 
    cnt_words = Counter(word_list)
    max_freq = cnt_words.most_common(1)[0][1]
    return max_freq/len(word_list), max_freq

# water_content
def getWaterContent(val, words_count):
    """
    Количество вхождение стоп слов в общее количество слов
    """
    word_list = tokenizer.tokenize(val)
    cnt_stopwords = sum(map(word_list.count, all_stopwords)) # количество вхождений стопслов в контент
    return cnt_stopwords/words_count

# density
def getDensityApply(val, qu, replace_city=True):
    txt = val.lower()
    qu = qu.lower()
    if replace_city:
        # обрезаем вхождение города
        city_name = replace_city_name
        qu = qu.replace(' в ' + city_name, '')
        qu = qu.replace(' ' + city_name, '')
    # разбиваем текст
    word_list = [w for w in tokenizer.tokenize(txt) if not w in all_stopwords]
    word_cnt = len(word_list)
    #print(word_list)
    #lemms = [morph.parse(w)[0].normal_form for w in word_list]
    qu_arr = np.array([])
    # каждое слово в запросе считаем отдельно
    for q in qu.split():
        qu_arr = np.append(qu_arr, len(re.findall(rf'{q}', txt)))
    cnt_qu = qu_arr.mean()
    #return cnt_qu/word_cnt, len(re.findall(rf'{qu}', txt))/word_cnt
    return cnt_qu/word_cnt


# tf_idf
def getTFIDF(density, qu):
    url = row['url']
    q = row['search_query_n']
    tf = df[df['url'] == url][q+'_density'].values[0]
    idf = qu_idf[q]
    return tf/idf