import openpyxl
from mongo import collection_raport, timeit


@timeit
def writing_result():
	def transport_list_in_string(incoming_list: list):
		"""Переводит список в строку"""
		result_string = ''
		for i in incoming_list:
			result_string = result_string + i + ','
		return result_string

	raport = collection_raport.find()

	wb = openpyxl.Workbook()
	wb.create_sheet(title='Результат обработки', index=0)
	sheet = wb['Результат обработки']

	count_collections_raport = collection_raport.estimated_document_count()
	count_write = 0

	while count_write < count_collections_raport:

		for item in raport:
			if count_write == 0:
				"""Добавляем первую строку в файл с названиями колонок"""
				product_id = 'product_id'
				full_description = 'full_description'
				rest_of_description = 'rest_of_description'
				verified_e_indexes = 'verified_e_indexes'
				verified_keywords = 'verified_keywords'
				total_list_e_indexes = 'total_list_e_indexes'

				list_data = [product_id, full_description, rest_of_description, verified_e_indexes,
							 verified_keywords, total_list_e_indexes]

				sheet.append(list_data)

				count_write += 1
			else:
				"""Записываем данные из базы в таблицу построчно // ниже первой строки"""
				count_write += 1

				product_id = item['product_id']
				full_description = item['full_description']
				rest_of_description = item['rest_of_description']
				verified_e_indexes = transport_list_in_string(item['verified_e_indexes'])
				verified_keywords = transport_list_in_string(item['verified_keywords'])
				total_list_e_indexes = transport_list_in_string(item['total_list_e_indexes'])

				list_data = [product_id,
							 full_description,
							 rest_of_description,
							 verified_e_indexes,
							 verified_keywords,
							 total_list_e_indexes]

				print(count_write, list_data)
				sheet.append(list_data)

	wb.save('Result/result.xlsx')
	del count_write


if __name__ == "__main__":
	writing_result()
