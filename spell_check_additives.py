"""Проверка правописания добавок:
1. проверка написания кода добавки:
1.1. проверка и исправление всех заглавных букв 'E' на английские
1.2. проверка и исправление всех кодов написание Е слитно с номером кода добавки == ликвидация пробелов
"""
import openpyxl
import re

excel = 'Additives/Additives+.xlsx'


def search_and_correct_rus_letters(document):
	"""находит и кооректирует русскую букву Е заменяя ее на англ."""
	wb = openpyxl.load_workbook(excel)
	sheet = wb.active
	for row in sheet:
		"""читаем таблицу построчно"""
	additive_code = row[0].value
	"""получаем значение первой ячейки в строке"""
	additive_cell_coordinate = row[0].coordinate
	"""получаем первую колонку"""
	first_literal = additive_code[:1]
	if first_literal == 'Е':
		"""Ищем русские буквы 'Е' в названиях кодов"""
		first_literal = 'E'
		"""присваиваем первую букву англ."""
		regex = r"(?!Е).*"
		'''опеределяем часть строки которая не русская "Е" через шаблон'''
		matches = re.search(regex, additive_code)
		"""производим поиск по шабоону"""
		second_part_code = matches.group()
		"""присваиваем искомую часть переменной"""
		new_additive = first_literal + second_part_code
		"""присваиваем занчение с англ. буквой Е """
		sheet[additive_cell_coordinate] = new_additive
		"""приваиваем новое значение в ячейку с координатами"""
		wb.save(excel)
		"""записываем данные в файл"""
		print(f'Найдена русская буква "Е" в {additive_code} в ячейке {additive_cell_coordinate}')

	print('Русские буквы Е в кодах добавок не обнаружены')
	print('==============================================')


def search_andcorrect_spaces(docement):
	"""находит и исправляет пробелы в названии кода добавки"""
	wb = openpyxl.load_workbook(docement)
	sheet = wb.active
	for row in sheet:
		"""читаем таблицу построчно"""
		additive_code = row[0].value
		"""получаем значение первой ячейки в строке"""
		additive_cell_coordinate = row[0].coordinate
		"""получаем первую колонку"""
		regex = r"(?!E)\s"
		"""шаблон пробела после первой буквы"""
		matches = re.search(regex, additive_code)
		"""применяем шаблон к строке в ячейке"""
		if matches:
			new_additive = additive_code.replace(' ', '')
			"""полное название кода без пробела"""
			sheet[additive_cell_coordinate] = new_additive
			"""приваиваем новое значение в ячейку с координатами"""
			wb.save(excel)
			"""записываем данные в файл"""

			print(f'Найдены пробелы в {additive_code} в ячейке {additive_cell_coordinate}')

	print('Пробелы в кодах добавок не обнаружены')


if __name__ == '__main__':
	search_and_correct_rus_letters(document=excel)
	search_andcorrect_spaces(docement=excel)
