import openpyxl
import os

from pymongo.errors import WriteError

from mongo import collection_additives
from pymongo import errors

"""Файл с добавками для загрузки в базу данных"""
additives_dir = 'Additives'
structure_dir = 'Structure'


def name_of_file(path: str):
	"""Открывает файл и отдает имя файла, принимает путь к файлу в соотеветствющей дирректории"""
	list_dir = os.listdir(path=path)
	for item in list_dir:
		name_of_file = item
	return name_of_file


def active_sheet(name_dir: str):
	"""Получает активную таблицу"""
	xlsx_file = name_of_file(name_dir)
	"""Передаем имя файла"""
	path = additives_dir + '/' + xlsx_file
	"""Получаем путь к файлу"""
	wb = openpyxl.load_workbook(path)
	"""Получаем рабочую книгу - workbook"""
	active_sheet = wb.active
	"""Получаем активную вкладку рабочей книги"""
	return active_sheet

#TODO Сделать доступ к файлу относительным!!!

# additives_sheet = active_sheet(additives_dir)
additives_sheet = 'Additives/Добавки_Additives.xlsx'


def upload_and_update_additives(document):
	wb = openpyxl.load_workbook(document)
	sheet = wb.active

	excel_titles = {'additive': 'E-добавка (код)', 'keyword': 'Название'}
	"""название полей в документе - требуется жесткое соответствие"""

	class Additives(object):
		def __init__(self) -> None:
			self.id = None
			self.additive = None
			self.keyword = {}

	additives = Additives()

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
			additives.id = count
			additives.additive = str(row[titles[excel_titles['additive']]].value)
			additives.keyword = str(row[titles[excel_titles['keyword']]].value).split(', ')

			query = {
				'_id': additives.id,
				'additive': additives.additive,
				'keywords': additives.keyword
			}

			try:
				collection_additives.replace_one({"additive": additives.additive}, query, upsert=True)
				"""добавляем/обновляем данные в коллекции (обновляем по полю добавки)"""
				print(query)
			except (WriteError):
				print(Exception(WriteError))


if __name__ == '__main__':
	upload_and_update_additives(document=additives_sheet)
