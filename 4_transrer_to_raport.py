import datetime

from mongo import collection_stucture, collection_raport, collection_additives, consolidated, timeit


@timeit
def collect_raport():
	"""Собираем данные и передаем их в коллецию Raport"""

	def replace_expression(expressions: list, description: str):
		"""Удаляет из строке выражения из списка"""
		for item in expressions:
			description = description.replace(item, '')
		return description

	stucture = collection_stucture.find()
	list_verified_keywords = []  # Список подтвержденных ключевых слов
	list_verified_e_indexes = []  # Список подтвержденных Е-индексов
	total_list_e_indexes = []  # Общий список Е-индексов подтвержденных и комплементарных ключевым словам

	for item in stucture:
		"""Копируем документ во временную таблицу для последующего поиска совпадений e-index и keywords"""
		id = item['_id']
		product_id = item['product_id']
		full_description = item['description']

		tmp_description = full_description
		print(f'Обрабатывается id {id}')

		######## Разбираем данные из Additives: e-index: str, keywords: list
		count_collection_additives = collection_additives.estimated_document_count()
		count_additives = 1

		while count_additives < count_collection_additives:
			try:
				additive = collection_additives.find_one({'_id': count_additives})
				e_index = additive['additive']
				list_keywords = additive['keywords']

				#############  Первыми обрабатываем Е-indexes == без вариантов сравнения заглавных и прописных букв

				if e_index in full_description:
					list_verified_e_indexes.append(e_index)
					total_list_e_indexes.append(e_index)
			except Exception as e:
				# print(e)
				pass

			#############  Проверяем наличие Keywords в описании

			for keyword in list_keywords:
				if keyword != 'None':
					temp_list_keywords = []
					title = keyword.title()
					lower = keyword.lower()
					temp_list_keywords.append(title)
					temp_list_keywords.append(lower)
					for keyword in temp_list_keywords:
						if keyword in tmp_description:
							list_verified_keywords.append(keyword)
							total_list_e_indexes.append(e_index)
			count_additives += 1

		rest_e_index_description = replace_expression(list_verified_e_indexes, full_description)
		rest_of_description = replace_expression(list_verified_keywords, rest_e_index_description)

		#############  Записываем результаты
		"""Добавляем e-index по которому найдено совпадение в список"""
		consolidated.id = id
		consolidated.one_product_id = product_id
		consolidated.list_e_index = list_verified_e_indexes
		consolidated.list_keywords = list_verified_keywords
		consolidated.full_description = full_description
		consolidated.rest_of_description = rest_of_description
		consolidated.total_list_e_indexes = total_list_e_indexes

		data_e_index_temporary = {
			'_id': consolidated.id,
			'product_id': consolidated.one_product_id,
			'full_description': consolidated.full_description,
			'rest_of_description': consolidated.rest_of_description,
			'verified_e_indexes': consolidated.list_e_index,
			'verified_keywords': consolidated.list_keywords,
			'total_list_e_indexes': consolidated.total_list_e_indexes,
		}

		print(f'data_e_index_temporary {data_e_index_temporary}')
		collection_raport.replace_one({'_id': consolidated.id, }, data_e_index_temporary, upsert=True)

		list_verified_e_indexes.clear()
		list_verified_keywords.clear()
		total_list_e_indexes.clear()


if __name__ == "__main__":
	collect_raport()
