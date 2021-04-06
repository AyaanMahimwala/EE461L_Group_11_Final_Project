from ..db_entry import DataSet
from ..mongo import MongoEntry
from .data_set_schema import DataSetSchema
from .data_set_schema import UserDataSetSchema

class DataSetService(object):
    """
    Called on init, sets the client which is an abstract 'DataSet' on the frontend
    and a mongodb entry on the backend. It also sets the 'user_id' so that we can 
    save user specific data_sets or settings.
    """

    DATASET_COLLECTION_NAME = "DataSet"

    def __init__(self):
        self.data_set_client = DataSet(adapter=MongoEntry(self.DATASET_COLLECTION_NAME))

    """
    Method that returns the count of data sets
    """
    def count_data_set(self):
        data_sets = list(self.data_set_client.find_all({})) or []
        if data_sets != []:
            #print(data_sets)
            return int(len(data_sets))
        else:
            return 0

    """
    Grabs all the data_sets for user by name
    """
    def find_all_data_sets_for(self, user_name):
        data_sets  = self.data_set_client.find_all({'user_name': self.user_name}) or []
        return [self.dump(data_set) for data_set in data_sets]

    """
    Grabs all the not private data_sets
    """
    def find_all_public_data_sets(self):
        data_sets  = self.data_set_client.find_all({'private': False}) or []
        return [self.dump(data_set) for data_set in data_sets]

    """
    Finds a specific data_set by name, ignores privacy
    """
    def find_data_set(self, data_set_name):
        data_set = self.data_set_client.find({'data_set_name': self.data_set_name})
        if data_set:
            return self.dump(data_set)
        else:
            return None

    """
    Creates a specific data_set, if the user_name field is provided then create a user data set
    Return true if sucessful create else false
    Ensures only unique data_set_name
    """
    def create_data_set_for(self, data_set_name, file_size, description, data_set_url, private = False, user_name = None):
        if self.find_data_set(data_set_name) == None:
            data_set = self.data_set_client.create(self.prepare_data_set(data_set_name, file_size, description, data_set_url, private, user_name))
            return True if data_set != None else False
        else:
            return False
    
    """
    Updates a specific data_set by name with new data
    If the name doesn't exist returns False as set not updated
    If it does update the set then returns true and changes reflected in db
    """
    def update_data_set_with(self, data_set_name, file_size, description, data_set_url, private = False, user_name = None):
        records_affected = 0
        if self.find_data_set(data_set_name) != None:
            records_affected = self.data_set_client.update(self.prepare_data_set(data_set_name, file_size, description, data_set_url, private, user_name))
        return True if records_affected > 0 else False

    """
    Deletes a specific data_set name if it exists
    """
    def delete_data_set_for(self, data_set_name):
        records_affected = self.data_set_client.delete({'data_set_name': self.data_set_name})
        return True if records_affected > 0 else False

    """
    Dumps all non-identifying info about the data_set
    """
    def dump(self, data_set):
        return DataSetSchema.dump(data_set)

    """
    Used to update/create data_set
    """
    def prepare_data_set(self, data_set_name, file_size, description, data_set_url, private, user_name):
        data_set = {}
        data_set['data_set_name'] = data_set_name
        data_set['file_size'] = file_size
        data_set['description'] = description
        data_set['data_set_url'] = data_set_url
        data_set['private'] = private
        if user_name != None:
            data_set['user_name'] = user_name
            schema = UserDataSetSchema()
        else:
            schema = DataSetSchema()
        return data_set
