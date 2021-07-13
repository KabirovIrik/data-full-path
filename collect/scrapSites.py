import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import csv
import urllib


chromedriver = 'd:/games/chrome/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
browser.set_page_load_timeout(15)

prev_domain = ''
cntr = 0
last = 781 # <<<< тут ошибка была
with open('urlSites.csv', encoding='utf-8') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';')
	for row in spamreader:
		url = row[0]

		if cntr < last: # <<<< тут ошибка была
			print('continue ', cntr, url)
			cntr +=1
			continue
		try:
			domain = url.split('//')[1].split('/')[0] # разбиваем урл и получаем домен
			domain_arr = domain.split('.')
			if len(domain_arr) == 3:
				domain_arr = domain_arr[1:]
				domain = '.'.join(domain_arr)
		except:
			domain = url

		if prev_domain == domain: # если предыдущий домен совпадает с текущим, то ждем
			print('waiting...')
			# ждем
			sleeping_time = random.uniform(0.1235, 0.5314)
			time.sleep(sleeping_time)
		try:
			browser.get(url)
			html = browser.page_source
			with open('sites_content.csv', 'a', encoding='utf-8', newline='') as to_csvfile:
				spamwriter = csv.writer(to_csvfile, delimiter=';')
				spamwriter.writerow([url, domain, html])

			prev_domain = domain
			print(cntr, url)
		except:
			print('fail ', cntr, url)
			with open('fail.csv', 'a', encoding='utf-8', newline='') as to_csvfile_fail:
				spamwriter_fail = csv.writer(to_csvfile_fail, delimiter=';')
				spamwriter_fail.writerow([url, domain])
		cntr += 1
"""
url
html
"""