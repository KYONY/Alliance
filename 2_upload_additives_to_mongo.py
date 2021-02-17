import openpyxl

from pymongo.errors import WriteError

from mongo import collection_additives, search_file_in_dir, timeit, consolidated

"""Файл с добавками для загрузки в базу данных"""
additives_dir = 'Additives'
structure_dir = 'Structure'

path = search_file_in_dir(additives_dir)

wb = openpyxl.load_workbook(path)
"""Получаем рабочую книгу - workbook"""
active_sheet = wb.active
"""Получаем активную вкладку рабочей книги"""

additives_sheet = search_file_in_dir(incoming_dir=additives_dir)


@timeit
def upload_and_update_additives(document):
	wb = openpyxl.load_workbook(document)
	sheet = wb.active

	excel_titles = {
		'additive': 'E-добавка (код)',
		'keyword': 'Название'
	}
	"""название полей в документе - требуется жесткое соответствие"""

	count = 0
	for i, row in enumerate(sheet):
		if i == 0:
			"""учитываем надписи первой строки но не заносим ее в БД"""
			titles = {}
			for row_number, title in enumerate(row):
				titles[title.value] = row_number

		elif i > 0:
			"""для строк 2 и бодее производим обработку данных """
			count += 1
			consolidated.id = count
			consolidated.one_e_index = str(row[titles[excel_titles['additive']]].value)
			consolidated.list_keywords = str(row[titles[excel_titles['keyword']]].value).split(', ')

			query = {
				'_id': consolidated.id,
				'additive': consolidated.one_e_index,
				'keywords': consolidated.list_keywords
			}

			try:
				collection_additives.replace_one({"additive": consolidated.one_e_index}, query, upsert=True)
				"""добавляем/обновляем данные в коллекции (обновляем по полю добавки)"""
				print(query)
			except (WriteError):
				print(Exception(WriteError))


if __name__ == '__main__':
	upload_and_update_additives(document=additives_sheet)
