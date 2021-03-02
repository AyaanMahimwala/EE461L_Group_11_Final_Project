import os
from pymongo import MongoClient

#COLLECTION_NAME = 'mongo_sets'

class MongoEntry(object):
    def __init__(self):
        mongo_uri = os.environ.get('MONGO_DB_URI')
        self.db = MongoClient(mongo_url).mongo_sets

    def find_all(self, selector):
        return self.db.mongo_sets.find(selector)
 
    def find(self, selector):
        return self.db.mongo_sets.find_one(selector)
 
    def create(self, set):
        return self.db.mongo_sets.insert_one(set)

    def update(self, selector, set):
        return self.db.mongo_sets.replace_one(selector, set).modified_count
 
    def delete(self, selector):
        return self.db.mongo_sets.delete_one(selector).deleted_count
