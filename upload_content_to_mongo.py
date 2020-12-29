import openpyxl
from mongo import collection_stucture, finish

wb = openpyxl.load_workbook('Structure/Содержание_Content.xlsx')
sheet = wb.active


for item in sheet.rows:
	id = item[0].value
	content = item[1].value
	data = {
		'_id': id,
		'content': content,
	}
	print(data)
	collection_stucture.insert_one(data).inserted_id

finish(command='Загрузка данных в базу завершена')


