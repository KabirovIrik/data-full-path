import csv

# список запросов в Уфе
quries_ufa = []
with open('ufa_queries.csv', encoding='utf-8') as csv_file:
	file = csv.reader(csv_file, delimiter=';')
	for row in file:
		quries_ufa.append(row[0])
if __name__ == "__main__":
	print(quries_ufa)
