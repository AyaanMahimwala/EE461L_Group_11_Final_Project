import os
from pymongo import MongoClient

DATABASE_NAME = "EE461L_Final_Project_DB"
DATABASE_HOST = os.environ.get('MONGO_DB_URI')

DATABASE_USERNAME = "EE461L_Database_Username"
DATABASE_PASSWORD = "EE461L_Database_Password"

class MongoEntry(object):
    def __init__(self, collection_name):
        try:
            my_client = MongoClient( DATABASE_HOST )
            my_client.test.authenticate( DATABASE_USERNAME , DATABASE_PASSWORD )
            self.my_db = my_client[DATABASE_NAME]
            self.my_collection = self.my_db[collection_name]

            print("[+] Database connected!")
        except Exception as e:
            print("[+] Database connection error!")
            raise e

    def find_all(self, selector):
        return self.my_collection.find(selector)
 
    def find(self, selector):
        return self.my_collection.find_one(selector)
 
    def create(self, set):
        return self.my_collection.insert_one(set)

    def update(self, selector, set):
        return self.my_collection.replace_one(selector, set).modified_count
 
    def delete(self, selector):
        return self.my_collection.delete_one(selector).deleted_count
