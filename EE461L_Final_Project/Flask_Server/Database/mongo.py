import os
from pymongo import MongoClient

COLLECTION_NAME = 'data_sets'

class MongoEntry(object):
    def __init__(self):
        mongo_url = os.environ.get('MONGO_URL')
        self.db = MongoClient(mongo_url).data_sets

    def find_all(self, selector):
        return self.db.data_sets.find(selector)
 
    def find(self, selector):
        return self.db.data_sets.find_one(selector)
 
    def create(self, kudo):
        return self.db.data_sets.insert_one(kudo)

    def update(self, selector, data_set):
        return self.db.data_sets.replace_one(selector, data_set).modified_count
 
    def delete(self, selector):
        return self.db.data_sets.delete_one(selector).deleted_count
