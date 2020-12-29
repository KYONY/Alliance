import openpyxl
import os
from mongo import collection_additives
from pymongo import errors

"""Файл с добавками для загрузки в базу данных"""
additives_dir = 'Additives'
structure_dir = 'Structure'


def name_of_file(path: str):
	"""Открывает файл и отдает имя файла, принимает путь к файлу в соотеветствющей дирректории"""
	list_dir = os.listdir(path=path)
	for item in list_dir:
		file = item
	return file

def active_sheet(name_dir:str):
	"""Получает активную таблицу"""
	xlsx_file = name_of_file(additives_dir)
	"""Передаем имя файла"""
	path = additives_dir + '/' + xlsx_file
	"""Получаем путь к файлу"""
	wb = openpyxl.load_workbook(path)
	"""Получаем рабочую книгу - workbook"""
	sheet = wb.active
	"""Получаем активную вкладку рабочей книги"""
	return sheet


additives_sheet = active_sheet(additives_dir)


def upload_additives_to_mongo(sheet):
	count = 0
	worksheet = sheet
	for item in worksheet.rows:
		"""Выводим данные построчно"""
		count += 1
		name = item[0].value
		keyword = item[1].value
		list_name = list(name)
		first_letter = list_name[0]
		if first_letter == 'Е':
			print(f'Русские буквы в {name}')
		else:
			print(f'Англ буквы в {name}')





		# data = {
		# 	'_id': count,
		# 	'name': name,
		# 	'keyword': keyword,
		# }
		# print(data)
		# collection_additives.insert_one(data).inserted_id


upload_additives_to_mongo(sheet=additives_sheet)


# if __name__ == 'main':
# 	upload_additives_to_mongo(sheet=additives_sheet)

