from ..db_entry import DataSet
from ..mongo import MongoEntry
from .data_set_schema import UserDataSetSchema
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv
from datetime import datetime
import os
import time
from random import randint

DATASET_COLLECTION_NAME = "DataSet"

class DataSetService(object):
    """
    Called on init, sets the client which is an abstract 'DataSet' on the frontend
    and a mongodb entry on the backend. It also sets the 'user_id' so that we can 
    save user specific data_sets or settings.
    """
    def __init__(self, user_id, data_set_client=DataSet(adapter=MongoEntry(DATASET_COLLECTION_NAME))):
        self.data_set_client = data_set_client
        self.user_id = user_id

        if not user_id:
            raise Exception("user id not provided")

    """
    Grabs all the data_sets
    """
    def find_all_data_sets(self):
        data_sets  = self.data_set_client.find_all({'user_id': self.user_id})
        return [self.dump(data_set) for data_set in data_sets]

    """
    Finds a specific data_set by id, whoever owns the id owns the set
    """
    def find_data_set(self, data_set_id):
        data_set = self.data_set_client.find({'user_id': self.user_id, 'data_set_id': data_set_id})
        return self.dump(data_set)

    """
    Creates a specific data_set by id, whoever owns the id owns the set
    """
    def create_data_set_for(self, user_data_set):
        self.data_set_client.create(self.prepare_data_set(user_data_set))
        return self.dump(user_data_set.data)
    
    """
    Updates a specific data_set by id, whoever owns the id owns the set, returns affected records
    """
    def update_data_set_with(self, data_set_id, user_data_set):
        records_affected = self.data_set_client.update({'user_id': self.user_id, 'data_set_id': data_set_id}, self.prepare_data_set(user_data_set))
        return records_affected > 0

    """
    Deletes a specific data_set by id, whoever owns the id owns the set
    """
    def delete_data_set_for(self, data_set_id):
        records_affected = self.data_set_client.delete({'user_id': self.user_id, 'data_set_id': data_set_id})
        return records_affected > 0

    """
    Dumps all non-identifying info about the data_set
    """
    def dump(self, data):
        return UserDataSetSchema(exclude=['user_id']).dump(data).data

    """
    Used to update/create data_set
    """
    def prepare_data_set(self, user_data_set):
        data = user_data_set.data
        data['user_id'] = self.user_id
        return data

    """
    This function webscrapes all datasets from the Physionet database and returns a list of all dataset descriptions.
    """
    def get_data_sets(self):
        page = "https://physionet.org/about/database/"
        page_html = urlopen(page).read()

        page_soup = soup(page_html, "html.parser")

        container = page_soup.findAll('a')      # All elements stored in container list
        container = container[14:len(container)-4]

        return container
