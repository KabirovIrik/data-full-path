import joblib, pickle
from convertInput import *

def getResponse(query_input, url):

    if USE_SELENIUM:
        browser.get(url)
        my_file = browser.page_source
    else:
        my_file = requests.get(url).text

    my_file = replaceCityName(my_file)
    textContent = get_lemm(getTextContent(my_file))


    df_q = pd.read_csv('queries_full.csv', sep=';')
    query = df_q[df_q['search_query'] == query_input]
    query_input_common = ' '.join([morph.parse(w)[0].normal_form for w in tokenizer.tokenize(query_input)]).replace(city_name.lower(), replace_city_name)


    data_to_model = {}
    data_to_model['freq'] = query['freq'].values[0] 
    data_to_model['query_results_count_num'] = query['query_results_count_num'].values[0] 
    title, descr, kw, data_to_model['len_mt'], data_to_model['len_md'], data_to_model['len_kw']   = getMeta(my_file)
    data_to_model['len_w_mt'] = getLenWords(title)
    data_to_model['len_w_md'] = getLenWords(descr)
    data_to_model['len_w_kw'] = getLenKeyWords(kw)
    data_to_model['words_count'], data_to_model['words_count_sw'] = getWordsCount(textContent)
    data_to_model['spamity'], data_to_model['max_spam'] = getSpamity(textContent)
    data_to_model['water_content'] = getWaterContent(textContent, data_to_model['words_count'])
    data_to_model['density'] = getDensityApply(textContent, query_input_common, replace_city=False)
    data_to_model['tf_idf'] = data_to_model['density']/qu_idf[query_input_common]


    list_columns = ['freq', 'query_results_count_num', 'len_mt', 'len_md', 'len_kw',
           'len_w_mt', 'len_w_md', 'len_w_kw', 'words_count', 'words_count_sw',
           'spamity', 'max_spam', 'water_content', 'tf_idf', 'density']
    predict_data = np.array([data_to_model[col] for col in list_columns]).reshape(1, -1)


    with open('query_dict_data.pkl', 'rb') as f:
        query_data = pickle.load(f)[query_input_common]
        rf_model = joblib.load(query_data['model'])

    data_to_model['predict'] = np.int(rf_model.predict_proba(predict_data)[0][0] * 100)
    data_to_model['q'] = query_data



    return data_to_model