import os
from pymongo import MongoClient

DATABASE_NAME = "database_name"
DATABASE_HOST = os.environ.get('MONGO_DB_URI')

DATABASE_USERNAME = "database_username"
DATABASE_PASSWORD = "database_password"

class MongoEntry(object):
    def __init__(self):
        try:
            my_client = pymongo.MongoClient( DATABASE_HOST )
            my_client.test.authenticate( DATABASE_USERNAME , DATABASE_PASSWORD )
            self.my_db = my_client[DATABASE_NAME]

            print("[+] Database connected!")
        except Exception as e:
            print("[+] Database connection error!")
            raise e

    def find_all(self, selector):
        return self.my_db.find(selector)
 
    def find(self, selector):
        return self.my_db.find_one(selector)
 
    def create(self, set):
        return self.my_db.insert_one(set)

    def update(self, selector, set):
        return self.my_db.replace_one(selector, set).modified_count
 
    def delete(self, selector):
        return self.my_db.delete_one(selector).deleted_count
