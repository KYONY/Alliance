import datetime
import pymongo
from pymongo.errors import OperationFailure

from mongo import finish, collection_stucture, collection_additives, collection_missing_additives, collection_final, \
	collection_e_additive, collection_k_additive, Consolidated, collection_product_id

raport = collection_final.find()
additives = collection_additives.find()
structure = collection_stucture.find()
e_additive = collection_e_additive.find()
k_additive = collection_k_additive.find()
product = collection_product_id.find()
consolidated = Consolidated()

"""Из коллекции Product_id берем product_id и full_description (сразу идет в query).
	 По product_id в коллекции K_additive забираем, если есть совпадения, keyword и relation_to_additive
	 По product_id в коллекции E_additive забираем, если есть совпадения, e_index
	 Записываем в базу данных: id == product_id, full_description, keyword {list}, relation_to_additive, e_index {list}
	 """


def collects_k_additives():
	"""Из коллекции Product_id берем product_id и full_description (сразу идет в query).
	 По product_id в коллекции K_additive забираем, если есть совпадения, keyword и relation_to_additive"""
	list_e_indexes = []
	list_keywords = []
	count = 0
	try:
		collection_k_additive.drop_index([('product_id', 'text')])
	except:
		print('В удалении индекса необходимость отсутствует =)')

	try:
		search_index = collection_k_additive.create_index([('product_id', 'text')], default_language='english')
		print(f'search_index {search_index}')
	except:
		print('Создание индекса collection_k_additive не удалось')

	for i in product:
		one_product_id = i['product_id']
		full_description = i['full_description']

		try:
			for j in collection_k_additive.find({"$text": {"$search": one_product_id}}):
				product_id_by_collection_k_additive = j['product_id']
				relation_to_additive = j['relation_to_additive']
				keyword = j['keyword']
				consolidated.one_product_id = i['product_id']

				list_e_indexes.append(relation_to_additive)
				consolidated.list_e_index = list_e_indexes

				list_keywords.append(keyword)
				consolidated.keywords = list_keywords
				consolidated.full_description = full_description

			if len(list_e_indexes) != 0 and len(list_keywords) != 0:

				query_for_final_collection = {
					'_id': consolidated.one_product_id,
					'one_product_id': consolidated.one_product_id,
					'e_additives': consolidated.list_e_index,  # list
					'keywords': consolidated.keywords,  # list
					'full_description': consolidated.full_description,
					# 'rest_of_description': consolidated.rest_of_description,
				}
				try:
					collection_final.replace_one({'_id': consolidated.one_product_id},
												  query_for_final_collection, upsert=True)
					count += 1
					print(count, i['product_id'], list_e_indexes, list_keywords, full_description)

				except Exception:
					print(f'Exception {Exception}')

			list_e_indexes.clear()
			list_keywords.clear()

		except (OperationFailure):
			print('OperationFailure: text index required for $text query')

	collection_k_additive.drop_index([('product_id', 'text')])


def collects_k_additives():
	"""Из коллекции Product_id берем product_id и full_description (сразу идет в query).
	 По product_id в коллекции E_additive забираем, если есть совпадения, e_index
	 Записываем в базу данных: id == product_id, full_description, keyword {list}, relation_to_additive, e_index {list}
	 """
	list_e_indexes = []
	count = 0
	try:
		collection_e_additive.drop_index([('product_id', 'text')])
	except:
		print('В удалении индекса необходимость отсутствует =)')

	try:
		search_index = collection_e_additive.create_index([('product_id', 'text')], default_language='english')
		print(f'search_index {search_index}')
	except:
		print('Создание индекса collection_k_additive не удалось')

	for i in product:
		one_product_id = i['product_id']
		full_description = i['full_description']

		try:
			for j in collection_e_additive.find({"$text": {"$search": one_product_id}}):
				e_index_by_collection_e_additive = j['e_index']

				list_e_indexes.append(e_index_by_collection_e_additive)

			if len(list_e_indexes) != 0:

				item_raport = collection_final.find_one({'one_product_id': one_product_id})
				one_product_id = item_raport['one_product_id']
				e_indexes = item_raport['e_additives']
				keywords = item_raport['keywords']
				full_description = item_raport['full_description']

				result_e_indexes = list_e_indexes + e_indexes

				consolidated.one_product_id = one_product_id
				consolidated.list_e_index = result_e_indexes
				consolidated.keywords = keywords
				consolidated.full_description = full_description

				query_for_final_collection = {
					'_id': consolidated.one_product_id,
					'one_product_id': consolidated.one_product_id,
					'e_additives': consolidated.list_e_index,  # list
					'keywords': consolidated.keywords,  # list
					'full_description': consolidated.full_description,
					# 'rest_of_description': consolidated.rest_of_description,
				}
				try:
					collection_final.replace_one({'_id': consolidated.one_product_id},
												  query_for_final_collection, upsert=True)
					count += 1
					print(count, one_product_id)

				except Exception:
					print(f'Exception - запись в collection_final   {Exception}')

				count += 1
			# print(count, one_product_id, consolidated.list_e_index )

			list_e_indexes.clear()

		except Exception:
			print(f'Exception - поиск в collection_e_additive   {Exception}')

	collection_e_additive.drop_index([('product_id', 'text')])


if __name__ == '__main__':
	start_time = datetime.datetime.now()
	date_now = datetime.datetime.now().strftime("%d-%m-%Y")

	# collects_k_additives()
	# collects_k_additives()

	print('')
	end_time = datetime.datetime.now()
	print(f'Duration: {(end_time - start_time)}')
	print('Колличество обработанных позиций k_additive = ', collection_final.estimated_document_count())
	finish('Работа с базой данных завершена')
