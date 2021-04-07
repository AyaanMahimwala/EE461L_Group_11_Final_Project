import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

from ..db_entry import DataSet
from ..mongo import MongoEntry
from .hardware_set_schema import HardwareSetSchema

class HardwareSetService(object):
    """
    Called on init, sets the client which is an abstract 'HardwareSet' on the frontend
    and a mongodb entry on the backend.
    """

    HARDWARESET_COLLECTION_NAME = "HardwareSet"

    def __init__(self):
        self.hardware_set_client = DataSet(adapter=MongoEntry(self.HARDWARESET_COLLECTION_NAME))

    """
    Method that returns the count of hardware sets
    """
    def count_hardware_set(self):
        hardware_sets = list(self.hardware_set_client.find_all({})) or []
        if hardware_sets != []:
            #print(hardware_sets)
            return int(len(hardware_sets))
        else:
            return 0

    """
    Grabs all the not private hardware_sets
    """
    def find_all_hardware_sets(self):
        hardware_sets = self.hardware_set_client.find_all({}) or []
        return JSONEncoder().encode(hardware_sets)

    """
    Finds a specific hardware_set by name
    """
    def find_hardware_set(self, hardware_set_name):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
        return JSONEncoder().encode(hardware_set)


    """
    Creates a specific hardware_set
    Return true if sucessful create else false
    Ensures only unique hardware_set_name
    """
    def create_hardware_set_for(self, hardware_set_name, capacity, description, price_per_unit):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
        if hardware_set == None:
            hardware_set = self.hardware_set_client.create(self.prepare_hardware_set(hardware_set_name, capacity, description, price_per_unit))
            return True if hardware_set != None else False
        else:
            return False
    
    """
    Updates a specific hardware_set by name with new hardware
    If the name doesn't exist returns False as set not updated
    If it does update the set then returns true and changes reflected in db
    """
    def update_hardware_set_with(self, hardware_set_name, capacity, description, price_per_unit):
        records_affected = 0
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
        if hardware_set != None:
            records_affected = self.hardware_set_client.update({'hardware_set_name': hardware_set_name}, self.prepare_hardware_set(hardware_set_name, capacity, description, price_per_unit))
        return True if records_affected > 0 else False

    """
    Deletes a specific hardware_set name if it exists
    """
    def delete_hardware_set_for(self, hardware_set_name):
        records_affected = self.hardware_set_client.delete({'hardware_set_name': hardware_set_name})
        return True if records_affected > 0 else False

    """
    Dumps all non-identifying info about the hardware_set
    """
    def dump(self, hardware_set):
        hardware_set_dump = None
        if hardware_set != None:
            schema = DataSetSchema(exclude=['_id'])
            hardware_set_dump = schema.dump(hardware_set)
            print(hardware_set_dump, type(hardware_set_dump))
        return hardware_set_dump

    """
    Used to update/create hardware_set
    """
    def prepare_hardware_set(self, hardware_set_name, file_size, description, hardware_set_url, private, user_name):
        hardware_set = {}
        hardware_set['hardware_set_name'] = hardware_set_name
        hardware_set['file_size'] = file_size
        hardware_set['description'] = description
        hardware_set['hardware_set_url'] = hardware_set_url
        hardware_set['private'] = private
        hardware_set['user_name'] = user_name
        schema = DataSetSchema()
        result = schema.load(hardware_set)
        return result

