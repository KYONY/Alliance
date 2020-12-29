from mongo import collection_stucture, collection_additives

def parses_content(string):
	"""Принимает строку и отдает отдельные элементы списка в виде одиночных слов во вновь сформированном списке"""
	string_split = string.split(',')
	count = 0
	list_structure = []
	for i in string_split:
		count += 1
		item = (len(i.split()))
		if item < 2:
			list_structure.append(i)

		if item > 1:
			for j in string_split[count - 1].split():
				list_structure.append(j)
	return list_structure


for i in collection_additives.find():
	additive = i['name']
	# print(additive)
	for j in collection_stucture.find():
		content = j['content']
		# print(content)
		list_content = parses_content(content)
		for k in list_content:
			if k == additive:
				print(f'Найдена добавка {additive}')


# tmp_additive = 'Е220'
# print(type(tmp_additive))
#
# tmp = collection_stucture.find_one(filter={'_id': 1588100})
# list_tmp = tmp['content'].split()
#
# for i in list_tmp:
# 	print(type(i), i)
# 	if i == tmp_additive:
# 		print('=)!!!!!!!!!!')
# 	else:
# 		print('=(')

string = "Ниже приведен пример создания новой рабочей книги, в которой для шрифта, используемого в ячейке A1, устанавливается шрифт Arial, красный цвет, курсивное начертание и размер 24 пункта"
tmp_split = string.split(',')

# print((tmp_split[1].split()))





# for item in tmp_split:
# 	print(item)
# 	if len(item.split()) > 1:
