import json
from bson import ObjectId
from datetime import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

from ..db_entry import DataSet
from ..mongo import MongoEntry
from .hardware_set_schema import HardwareSetSchema
from .hardware_set_schema import CheckOutHardwareSetSchema

class HardwareSetService(object):
    """
    Called on init, sets the client which is an abstract 'HardwareSet' on the frontend
    and a mongodb entry on the backend.
    """

    HARDWARESET_COLLECTION_NAME = "HardwareSet"
    HARDWARESET_TICKETS_COLLECTION_NAME = "HardwareSetTickets"

    def __init__(self):
        self.hardware_set_client = DataSet(adapter=MongoEntry(self.HARDWARESET_COLLECTION_NAME))
        self.hardware_set_tickets = DataSet(adapter=MongoEntry(self.HARDWARESET_TICKETS_COLLECTION_NAME))

    def copy_hardware_set(self, hardware_set):
        dict = {}
        dict["hardware_set_name"] = hardware_set["hardware_set_name"]
        dict["description"] = hardware_set["description"]
        dict["price_per_unit"] = hardware_set["price_per_unit"]
        dict["capacity"] = hardware_set["capacity"]
        dict["availability"] = hardware_set["availability"]

        return dict


    ### ADMIN INTERFACE FOR HARDWARE SET MANAGEMENT ###

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
    Grabs all the hardware_sets
    """
    def find_all_hardware_sets(self):
        hardware_sets = self.hardware_set_client.find_all({}) or []
        names = []
        for hardware_set in hardware_sets:
            names.append(hardware_set["hardware_set_name"])
        return names

    """
    Finds a specific hardware_set by name
    """
    def find_hardware_set(self, hardware_set_name):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name}) or {}
        hardware_set = self.copy_hardware_set(hardware_set)
        print("Found set : {} of type {}".format(hardware_set, type(hardware_set)))
        if hardware_set != {}:
            return hardware_set
        else:
            hardware_set = {
                "hardware_set_name" : "No Name", 
                "capacity": 0,
                "availability": 0,
                "description": "No desciption.",
                "price_per_unit": 0.0
            }
            return hardware_set

    """
    Creates a specific hardware_set
    Return true if sucessful create else false
    Ensures only unique hardware_set_name
    """
    def create_hardware_set_for(self, hardware_set_name, capacity, description, price_per_unit):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
        if hardware_set == None:
            hardware_set = self.hardware_set_client.create(self.prepare_hardware_set(hardware_set_name, capacity, capacity, description, price_per_unit))
            return True if hardware_set != None else False
        else:
            return False
    
    """
    Updates a specific hardware_set by name with new hardware
    If the name doesn't exist returns False as set not updated
    If it does update the set then returns true and changes reflected in db
    Migrates tickets to the updated set without deletion where possible, else
    Deletes the newest tickets until capacity gap met (aka some cluster capacity or entire cluster taken offline)
    """
    def update_hardware_set_with(self, hardware_set_name, capacity, description, price_per_unit):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
        if hardware_set != None:
            # Grab all the tickets for the modified set
            checkout_hardware_set = list(self.hardware_set_client.find_all({'hardware_set_name': hardware_set_name})) or []
            print(checkout_hardware_set, type(checkout_hardware_set))
            # sort on timestamp so we know what to delete first, largest timestamp means newest so reverse order
            checkout_hardware_set = sorted(checkout_hardware_set, key = lambda lis: lis['ticket_creation_timestamp'], reverse=True)
            
            # Get the previous capacity
            previous_capacity = hardware_set.get('capacity')
            # Get the current availability
            availability = hardware_set.get('availability')

            # Delete any tickets in deleted clusters
            for key, value in previous_capacity.items():
                if key not in capacity:
                    # Cluster was deleted
                    # Remove from availibility, this will raise KeyError if the key does not exist which should not happen
                    del availability[key]
                    deleted_cluster_tickets = list(self.hardware_set_client.find_all({'hardware_set_name': hardware_set_name, 'cluster_name': key})) or []
                    for ticket in deleted_cluster_tickets:
                        user_name_to_delete = ticket.get('user_name')
                        # Delete this ticket
                        delete_ticket(hardware_set_name, key, user_name_to_delete)

            for key, value in capacity.items():
                # iterate over key value pairs
                if key not in previous_capacity:
                    # If this is a new cluster, init availability to full
                    availability[key] = value
                elif value < previous_capacity[key]:
                    # Theres a decrease in capacity
                    # Check if the availability can meet the capacity gap/shortage
                    difference = (previous_capacity[key] - value) - availability[key]
                    if difference >= 0:
                        # We took from the remaining availability so set it to 0
                        availability[key] = 0
                    # Set an index into the sorted list of tickets
                    index = 0
                    while difference > 0:
                        # Checkin the newest tickets until the capacity gap is filled
                        user_name_to_delete = checkout_hardware_set[index].get('user_name')
                        delete_ticket(hardware_set_name, key, user_name_to_delete)
                        # prepare for checkin of the next ticket
                        index = index + 1

            # Do the update with new migrated info, this should always return true, check for posterity
            records_affected = self.hardware_set_client.update({'hardware_set_name': hardware_set_name}, self.prepare_hardware_set(hardware_set_name, capacity, availability, description, price_per_unit))
            return True if records_affected > 0 else False
        else:
            return False

    """
    Deletes a specific hardware_set name if it exists
    """
    def delete_hardware_set_for(self, hardware_set_name):
        records_affected = self.hardware_set_client.delete({'hardware_set_name': hardware_set_name})
        if records_affected > 0:
            # Delete any open resource tickets
            self.hardware_set_tickets.delete({'hardware_set_name': hardware_set_name})
        return True if records_affected > 0 else False

    """
    Used to update/create hardware_set
    """
    def prepare_hardware_set(self, hardware_set_name, capacity, availability, description, price_per_unit):
        hardware_set = {}
        hardware_set['hardware_set_name'] = hardware_set_name
        hardware_set['capacity'] = capacity
        hardware_set['availability'] = availability
        hardware_set['description'] = description
        hardware_set['price_per_unit'] = price_per_unit
        schema = HardwareSetSchema()
        result = schema.load(hardware_set)
        return result

    ### CHECKOUT HARDWARE SET TICKETS ###

    """
    Method that returns the count of hardware set tickets checked out
    """
    def count_checkout_hardware_set(self):
        checkout_hardware_sets = list(self.hardware_set_tickets.find_all({})) or []
        if checkout_hardware_sets != []:
            #print(hardware_sets)
            return int(len(checkout_hardware_sets))
        else:
            return 0

    """
    Helper function to error check ticket requests
    Should ensure the requested resource is entirely available
    Returns True if ticket passes check else False
    """
    def check_ticket(self, hardware_set_name, unit_amount):
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name}) or {}
        if hardware_set != {}:
            availability = hardware_set.get('availability')
            if unit_amount <= availability:
                return True
            else:
                return False
        else:
            return False

    """
    Grabs all the tickets for user
    """
    def find_tickets_for(self, user_name):
        tickets = self.hardware_set_tickets.find_all({'user_name': user_name}) or []
        list_tickets = []
        for ticket in tickets:
            list_tickets.append("You, " + ticket.get('user_name') + ", checked out " + str(ticket.get('unit_amount')) + " from set " + ticket.get('hardware_set_name') + " for " +  str(ticket.get('price_per_unit')))
        return list_tickets

    """
    Method for users to checkout resources on a ticket by hardware set name
    Provide the amount to checkout
    Will reserve this amount until payment is collect
    Failed payment can simply call the delete
    """
    def create_ticket(self, hardware_set_name, unit_amount, user_name):
        unit_amount = int(unit_amount)
        if self.check_ticket(hardware_set_name, unit_amount) == True:
            # Cluster resources available
            # Need to get the harware set to get the price for ticket
            hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name}) or {}
            if hardware_set == {}:
                return False
            old_ticket = self.hardware_set_tickets.find({'hardware_set_name': hardware_set_name, 'user_name': user_name}) or {}
            if old_ticket != {}:
                # Combine tickets
                self.delete_ticket(hardware_set_name, user_name)
                ticket = self.hardware_set_tickets.create(self.prepare_ticket(hardware_set_name, unit_amount + old_ticket.get('unit_amount'), hardware_set.get('price_per_unit'), user_name))
            else:
                ticket = self.hardware_set_tickets.create(self.prepare_ticket(hardware_set_name, unit_amount, hardware_set.get('price_per_unit'), user_name))
            # Update availability
            hardware_set["availability"] = hardware_set.get('availability') - unit_amount
            self.hardware_set_client.update({'hardware_set_name': hardware_set_name}, hardware_set)
            return True
        else:
            return False

    """
    Method for user to change their ticket resource amount
    Can migrate cluster if its available
    Not sure if I want to implement this yet as there are arguement for not having it making sense
    """
    def update_ticket(self, hardware_set_name, unit_amount, user_name):
        unit_amount = int(unit_amount)
        old_ticket = self.hardware_set_tickets.find({'hardware_set_name': hardware_set_name, 'user_name': user_name}) or {}
        if old_ticket == {}:
            # Somehow got bad request just make a ticket
            return self.create_ticket(hardware_set_name, unit_amount, user_name)
        # Delete if 0
        if unit_amount == 0:
            return self.delete_ticket(hardware_set_name, user_name)
        # We must have an old ticket, pretend like we check back in and make new
        # Check we have the availability
        new_unit_amount = unit_amount - old_ticket.get('unit_amount')
        if self.check_ticket(hardware_set_name, new_unit_amount) == True:
            # Cluster resources available
            # Need to get the harware set to get the price for ticket
            hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name})
            # Make new ticket
            self.delete_ticket(hardware_set_name, user_name)
            return self.create_ticket(hardware_set_name, unit_amount, user_name)
        else:
            return False

    """
    Method for users (or payment portal bail out) to free/delete hardware resource tickets
    Also used above by the migrates in update function
    """
    def delete_ticket(self, hardware_set_name, user_name):
        # Need to get the harware set to get the price for ticket
        hardware_set = self.hardware_set_client.find({'hardware_set_name': hardware_set_name}) or {}
        if hardware_set == {}:
            return False
        old_ticket = self.hardware_set_tickets.find({'hardware_set_name': hardware_set_name, 'user_name': user_name}) or {}
        if old_ticket == {}:
            # Bad req
            return False
        unit_amount = old_ticket.get('unit_amount')
        # Update availability
        hardware_set["availability"] = hardware_set.get('availability') + unit_amount
        self.hardware_set_client.update({'hardware_set_name': hardware_set_name}, hardware_set)
        records_affected = self.hardware_set_tickets.delete({'hardware_set_name': hardware_set_name, 'user_name': user_name})
        return True if records_affected > 0 else False

    """
    Used to prepare a ticket
    """
    def prepare_ticket(self, hardware_set_name, unit_amount, price_per_unit, user_name):
        # current date and time
        now = datetime.now()
        ticket_creation_timestamp = datetime.timestamp(now)

        checkout_hardware_set = {}
        checkout_hardware_set['hardware_set_name'] = hardware_set_name
        checkout_hardware_set['unit_amount'] = unit_amount
        checkout_hardware_set['price_per_unit'] = price_per_unit
        checkout_hardware_set['user_name'] = user_name
        checkout_hardware_set['ticket_creation_timestamp'] = ticket_creation_timestamp
        schema = CheckOutHardwareSetSchema()
        result = schema.load(checkout_hardware_set)
        return result
