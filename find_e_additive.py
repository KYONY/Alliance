import datetime
from mongo import finish, collection_stucture, collection_additives, collection_missing_additives, \
	collection_e_additive


start_time = datetime.datetime.now()
"""Старт счетчика времени"""

date_now = datetime.datetime.now().strftime("%d-%m-%Y")
"""Текущаяя дата для _id коллекции отсутствующих добавок"""


class Consolidated(object):
	def __init__(self) -> None:
		self.id = None
		self.old_content = None
		self.update_content = None
		self.e_additives = {}
		self.keywords_additives = {}

consolidated = Consolidated()


# def search_by_keyword(collection: str, field: str, language: str, keyword: str):
# 	collection.create_index([(field, 'text')], default_language=language)
# 	for i in collection_stucture.find({"$text": {"$search": keyword}}):
# 		print(i)
# 	collection.drop_index([(field, 'text')])


id_of_product_with_additive = []
"""Спискок id продуктов которые содержат добавки"""
missing_additives = []
"""Спискок отсутствующих добавок Е... (англ)"""

for item in collection_additives.find():
	additive = item['additive']  # -> E110
	consolidated.e_additive = additive

	collection_stucture.create_index([('content', 'text')], default_language='english')
	"""CREATE INDEX"""
	for item in collection_stucture.find({"$text": {"$search": additive}}):
		consolidated.id = item['_id']
		consolidated.old_content = item['content']

		array_id = id_of_product_with_additive.append(item['_id'])

	try:
		if item['content']:
			query = {
				'_id': consolidated.e_additive,
				'id_product': id_of_product_with_additive
			}
			# print(query)
			collection_e_additive.replace_one({"_id": consolidated.e_additive}, query, upsert=True)

	except(KeyError):
		print(Exception(KeyError), f'среди описания товаров добавка "{consolidated.e_additive}" не найдена')

		missing_additives.append(consolidated.e_additive)
		"""добавляем данные в список отсутствующих добавок"""

	missing_additives_query = {
		'_id': date_now,
		'missing_additives': missing_additives
	}

	collection_missing_additives.replace_one({"_id": date_now}, missing_additives_query, upsert=True)
	"""добавляем/обновляем коллекцию отсутствующих добавок. Обновляем по полю id"""

	id_of_product_with_additive.clear()
	"""очищаем список id продуктов"""
	collection_stucture.drop_index([('content', 'text')])
	"""DROP INDEX"""

missing_additives.clear()
"""Очищаем список отсутствующих добавок"""


finish('Найденные добавки в базу данных загружены')

print('')
end_time = datetime.datetime.now()
"""Окончание таймера"""

print(f'Duration: {(end_time - start_time)}')

print('Количество товаров с описанием', collection_stucture.estimated_document_count())
print('Количество рассмотренных добавок', collection_additives.estimated_document_count())
print('Количество добавок отсутствующих в описании товаров', collection_missing_additives.estimated_document_count())

# search_by_phrase(collection=collection_stucture, field='content',language='russian', keyword='диоксид кремния')
