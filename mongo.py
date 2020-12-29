import os
import ssl
import pymongo as pymongo
from credentails import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client['Alliance']

collection_additives = db['Additives']
collection_stucture = db['Structure']

def finish(command:str):
	os.system(f'say {command}')



