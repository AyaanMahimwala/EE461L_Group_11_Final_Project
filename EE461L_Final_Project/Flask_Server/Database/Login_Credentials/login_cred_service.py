import hashlib
import base64
import bcrypt
from cryptography.fernet import Fernet
import os.path

from ..db_entry import DataSet
from ..mongo import MongoEntry
from .login_cred_schema import LoginSetSchema

class LoginSetService():
    """
    Sets the client which is an abstract 'LoginSet' on the frontend
    and a mongodb entry on the backend.
    """

    SALT_ROUNDS = 16
    LOGIN_COLLECTION_NAME = "LoginSet"

    def __init__(self):
        self.key = ""
        self.login_set_client = DataSet(adapter=MongoEntry(self.LOGIN_COLLECTION_NAME))

    """
    Generates a key and save it into a file
    If you delete the file its gg for all that data mapped to that key
    """
    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        self.key = key
        return key

    """
    Load the previously generated key or make a new one if first call
    """
    def load_key(self):
        try:
            if self.key == "":
                key_file = open("secret.key", "rb")
                # exists
                self.key = key_file.read()
                key_file.close()
                return self.key
            else:
                return self.key
        except FileNotFoundError:
            # doesn't exist
            print("CREATING NEW KEY!!!")
            return self.generate_key()

    """
    Encrypts a message
    """
    def encrypt_message(self, message):
        key = self.load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        #print(encrypted_message)
        return encrypted_message

    """
    Decrypts an encrypted message
    """
    def decrypt_message(self, encrypted_message):
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        decoded_message = decrypted_message.decode()

        #print(decrypted_message.decode())
        return decoded_message

    """
    Hash a password for the first time
    Using bcrypt, the salt is saved into the hash itself preventing rainbow table attacks
    We use sha256 and encode using base 64 to bypass the max length problems of blowfish
    """
    def get_hashed_password(self, plain_text_password):
      return bcrypt.hashpw(base64.b64encode(hashlib.sha256(str(plain_text_password).encode()).digest()), bcrypt.gensalt(rounds = self.SALT_ROUNDS))

    """
    Check hashed password. Using bcrypt, the salt is saved into the hash itself
    """
    def check_password(self, plain_text_password, hashed_password):
      return bcrypt.checkpw(base64.b64encode(hashlib.sha256(str(plain_text_password).encode()).digest()), hashed_password)

    """
    Method that returns the count of login sets
    """
    def count_login_set(self):
        login_sets = list(self.login_set_client.find_all({})) or []
        if login_sets != []:
            #print(login_sets)
            return int(len(login_sets))
        else:
            return 0

    """
    Finds a specific login_set by user_id (client side encrypted before send off)
    Could use find_one but want the database to be ensured to be unique users
    """
    def find_login_set(self, user_id):
        # Get users
        #print(self.login_set_client.find_all({}))
        login_sets = list(self.login_set_client.find_all({})) or []
        #print(login_sets, type(login_sets))
        if login_sets != []:
            #print("theres an entry")
            #print(login_set.get('user_id'), type(login_set.get('user_id')))
            for login_set in login_sets:
                if (self.decrypt_message(login_set.get('user_id')) == user_id):
                    return "True"
        return "False"

    """
    Creates a specific login_set with an encrypted user_id and hashed password if new user
    """
    def create_login_set_for(self, user_id, password):
        #print("create")
        if self.find_login_set(user_id) == "False":
            # Encrypt
            user_id = self.encrypt_message(str(user_id))
            # Hash
            password = self.get_hashed_password(str(password))
            #print("making new user")
            login_set = self.login_set_client.create(self.prepare_login_set(user_id, password))
            #print(login_set)
            #print("True" if login_set != None else "False")
            return "True" if login_set != None else "False"
        else:
            #print("user already exists")
            return "False"
    
    """
    Updates a specific login_set by user_id with new password, returns records affected which should be 1
    """
    def update_login_set_with(self, user_id, password):
        records_affected = 0
        # Get users
        login_sets = list(self.login_set_client.find_all({})) or []
        #print(login_set, type(login_set))
        if login_sets != []:
            for login_set in login_sets:
                if (self.decrypt_message(login_set.get('user_id')) == user_id):
                    # Encrypt
                    user_id = self.encrypt_message(str(user_id))
                    # Hash
                    password = self.get_hashed_password(str(password))
                    records_affected = self.login_set_client.update({'user_id': login_set.get('user_id')}, self.prepare_login_set(user_id, password))
        return "True" if records_affected > 0 else "False"

    """
    Deletes a specific login_set by user_id
    """
    def delete_login_set_for(self, user_id):
        records_affected = 0
        # Get users
        login_sets = list(self.login_set_client.find_all({})) or []
        #print(login_set, type(login_set))
        if login_sets != []:
            for login_set in login_sets:
                if (self.decrypt_message(login_set.get('user_id')) == user_id):
                    #print("Deleting : {}".format(login_set))
                    records_affected = self.login_set_client.delete({'user_id': login_set.get('user_id')})
                    #print(records_affected)
        return "True" if records_affected > 0 else "False"

    """
    Dumps login_set, doesn't make sense in this context but left in case
    """
    def dump(self, login_set):
        login_set_dump = LoginSetSchema.dump(login_set)
        return self.decrypt_message(login_set_dump.get('user_id'))

    """
    Used to update/create a login_set
    """
    def prepare_login_set(self, user_id, password):
        login_set = {}
        login_set['user_id'] = user_id
        login_set['password'] = password
        schema = LoginSetSchema()
        result = schema.load(login_set)
        return login_set

    """
    Return True if login creds match else False
    """
    def validate_login_set(self, plain_text_user_id, plain_text_password):
        # Get users
        login_sets = list(self.login_set_client.find_all({})) or []
        #print(login_sets, type(login_sets))
        if login_sets != []:
            #print(login_set)
            for login_set in login_sets:
                if (self.decrypt_message(login_set.get('user_id')) == plain_text_user_id):
                    return "True" if self.check_password(plain_text_password, login_set.get('password')) else "False"
