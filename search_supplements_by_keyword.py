import datetime

from pymongo.errors import CursorNotFound, OperationFailure, WriteError
from mongo import finish, collection_stucture, collection_additives, collection_k_additive, Consolidated, drop_index

stucture = collection_stucture.find()
additives = collection_additives.find()

start_time = datetime.datetime.now()
"""Старт счетчика времени"""

date_now = datetime.datetime.now().strftime("%d-%m-%Y")
"""Текущаяя дата для _id коллекции отсутствующих добавок"""

try:
	drop_index(field_of_document_for_search='content')
	"""удаления индекса, если предыдущий поиск был завершен не корректно"""
except:
	print("Поисковый индекс в удалении не нуждался =) ")

consolidated = Consolidated()
"""класс для сохранения в БД"""

product_id_with_keyword_additive = []
count = 0

for item in additives:
	additive = item['additive']
	keywords = item['keywords']

	for keyword in keywords:
		if keyword != 'None':
			keyword_for_search = '"' + keyword + '"'
			# print(keyword)

			collection_stucture.create_index([('content', 'text')], default_language='russian')
			"""создаем индекс для поиска в БД"""

			for i in collection_stucture.find(
					{"$text": {"$search": keyword_for_search}},
					{'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})]):
				product_id = i['_id']
				content = i['content']

				product_id_with_keyword_additive.append(product_id)
				consolidated.product_id = product_id_with_keyword_additive

			consolidated.id = count
			consolidated.keyword_additive = keyword
			consolidated.relation_to_additive = additive

			if consolidated.product_id:

				count += 1
				k_additive_query = {
					'_id': consolidated.id,
					'product_id': consolidated.product_id,
					'keyword': consolidated.keyword_additive,
					'relation_to_additive': consolidated.relation_to_additive,
				}
				print(k_additive_query)

				try:
					collection_k_additive.replace_one({'relation_to_additive': consolidated.relation_to_additive},
													  k_additive_query, upsert=True)
				except (CursorNotFound):
					print('Exception(CursorNotFound)')
				except (WriteError):
					print('Exception(WriteError)')


			product_id_with_keyword_additive.clear()
		# consolidated.product_id.clear()

collection_stucture.drop_index([('content', 'text')])

finish('Найденные добавки в базу данных загружены')

print('')
end_time = datetime.datetime.now()
"""Окончание таймера"""

print(f'Duration: {(end_time - start_time)}')

print('Количество товаров с описанием', collection_stucture.estimated_document_count())
print('Количество рассмотренных добавок', collection_additives.estimated_document_count())
