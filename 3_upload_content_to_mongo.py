import datetime

import openpyxl
from mongo import collection_stucture, finish, search_file_in_dir, timeit


# TODO сделать так, чтоб при загрузке "отсекалась первая строка"

@timeit
def upload_content_to_mongo():
	incoming_dir = 'Structure'
	path = search_file_in_dir(incoming_dir=incoming_dir)
	wb = openpyxl.load_workbook(path)
	sheet = wb.active

	for item in sheet.rows:
		id = item[0].value
		description = item[1].value
		product_id = str(item[0].value)
		query = {
			'_id': id,
			'description': description,
			'product_id': product_id,
		}
		print(query)
		collection_stucture.replace_one({'_id': id}, query, upsert=True)


if __name__ == '__main__':
	upload_content_to_mongo()
