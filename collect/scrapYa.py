import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import csv
import urllib


def getUrl(lr, text):
    ya_url = 'https://yandex.ru/search/'
    f = { 'lr' : str(lr), 'text' : text}
    querYa = ya_url + '?' + urllib.parse.urlencode(f) 
    return querYa



def startParsing():
	is_error = False
	chromedriver = 'd:/games/chrome/chromedriver.exe'
	options = webdriver.ChromeOptions()
	options.add_argument('--no-sandbox') # Bypass OS security model
	options.add_argument('headless')  # для открытия headless-браузера
	browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)


	with open('../urls.csv', encoding='utf-8') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';')
		for row in spamreader:
			print(row[0])
			lenRow = len(row)
			lr = row[2] # номер региона
			for i in range(3, lenRow):
				print()
				print(row[i], "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<") # текст запроса
				print()
				url = getUrl(lr, row[i])
				browser.get(url)
				requiredHtml = browser.page_source
				for i in range(5):
					##----------------    собираем инфу
					links_list = browser.find_elements_by_css_selector(".serp-item")
					if len(links_list) == 0:
						is_error = True
						print('error', url)
						break ##----------------    если капча или типа того, то конец

					if i == 0: # с первой страницы берем количество резульатов
						with open('parse_q.csv', 'a', encoding='utf-8', newline='') as to_csvfile_q:
							spamwriter = csv.writer(to_csvfile_q, delimiter=';')
							serp_found = browser.find_element_by_css_selector(".serp-adv__found")
							# serp_displa = browser.find_element_by_css_selector(".serp-adv__displayed")
							spamwriter.writerow([serp_found.text, row[i], lr])
				

					with open('parse.csv', 'a', encoding='utf-8', newline='') as to_csvfile:
						spamwriter = csv.writer(to_csvfile, delimiter=';')
						cntr = 0 # счетчик реальных позиций 
						for link in links_list:
							link_text = link.text
							a_tag = link.find_element_by_css_selector('.link') # тег ссылки
							href = a_tag.get_attribute('href') # атрибут ссылки
							page_num = i
							position = link.get_attribute('data-cid')

							# ссылки могут принадлежать яндексу
							if not href is None:
								if 'yandex' in href:
									is_ya_url = 1
								else:
									is_ya_url = 0

							# ищем рекламу
							is_reklama = 0
							for label in link.find_elements_by_css_selector('.label'):
								if label.text == 'реклама':
									is_reklama = 1
									break

							# если не реклама и не яндекс-ссылка, то реальная позиция
							if is_reklama == 0 and is_ya_url == 0:
								real_pos = cntr + page_num * 10
								cntr += 1
							else:
								real_pos = position

							spamwriter.writerow([link_text, href, page_num, real_pos, position, is_reklama, is_ya_url, row[i]])
						


					##----------------    к следующей странице
					# ждем
					sleeping_time = random.uniform(1.023, 1.5314)
					time.sleep(sleeping_time)
					# получаем и кликаем кнопку "Дальше"
					next_btn = browser.find_element_by_css_selector(".pager__item_kind_next")
					webdriver.ActionChains(browser).click(next_btn).perform()

			if is_error == True:
				print('stop parsing')
				break

startParsing()