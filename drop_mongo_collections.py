from mongo import collection_additives


def drop_collections():
	collection_additives.drop()

	return print ('Collections was Droped!')


if __name__ == "__main__":
	drop_collections()
