import hashlib
import base64
import bcrypt
from cryptography.fernet import Fernet
import os.path

from ..db_entry import DataSet
from ..mongo import MongoEntry
from .login_cred_schema import LoginSetSchema

SALT_ROUNDS = 16
LOGIN_COLLECTION_NAME = "LoginSet"

class LoginSetService(object):
    """
    Sets the client which is an abstract 'LoginSet' on the frontend
    and a mongodb entry on the backend.
    """
    def __init__(self, login_set_client=DataSet(adapter=MongoEntry(LOGIN_COLLECTION_NAME))):
        self.login_set_client = login_set_client

    """
    Generates a key and save it into a file
    """
    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

    """
    Load the previously generated key or make a new one if first call
    """
    def load_key(self):
        try:
            key_file = open("secret.key", "rb")
        except FileNotFoundError:
            # doesn't exist
            return self.generate_key()
        else:
            # exists
            return key_file.read()
        finally:
            key_file.close()

    """
    Encrypts a message
    """
    def encrypt_message(self, message):
        key = load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        print(encrypted_message)

    """
    Decrypts an encrypted message
    """
    def decrypt_message(self, encrypted_message):
        key = load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)

        print(decrypted_message.decode())

    """
    Hash a password for the first time
    Using bcrypt, the salt is saved into the hash itself preventing rainbow table attacks
    We use sha256 and encode using baase 64 to bypass the max length problems of blowfish
    """
    def get_hashed_password(plain_text_password):
      return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), bcrypt.gensalt(rounds = SALT_ROUNDS))

    """
    Check hashed password. Using bcrypt, the salt is saved into the hash itself
    """
    def check_password(plain_text_password, hashed_password):
      return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), hashed_password)

    """
    Finds a specific login_set by user_id (client side encrypted before send off)
    Could use find_one but want the database to be ensured to be unique users
    """
    def find_login_set(self, user_id):
        login_set = self.login_set_client.find({'user_id': user_id})
        return self.dump(login_set)

    """
    Creates a specific login_set with an encrypted user_id and hashed password if new user
    """
    def create_login_set_for(self, user_id, password):
        user_id_query = self.login_set_client.find()
        if user_id not in user_id_query:
            login_set = self.login_set_client.create(self.prepare_login_set(user_id, password))
            return self.dump(login_set)
    
    """
    Updates a specific login_set by user_id with new password, returns records affected which should be 1
    """
    def update_login_set_with(self, user_id, password):
        records_affected = self.login_set_client.update({'user_id': user_id}, self.prepare_login_set(user_id, password))
        return records_affected == 0

    """
    Deletes a specific login_set by user_id
    """
    def delete_login_set_for(self, user_id):
        records_affected = self.login_set_client.delete({'user_id': user_id})
        return records_affected == 0

    """
    Dumps login_set
    """
    def dump(self, login_set):
        return LoginSetSchema.dump(login_set)

    """
    Used to update/create a login_set
    """
    def prepare_login_set(self, user_id, password):
        login_set = {}
        login_set['user_id'] = user_id
        login_set['password'] = password
        return login_set

    """
    Return True if login creds match else False
    """
    def validate_login_set(self, plain_text_user_id, plain_text_password):
        login_set = find_login_set(self.encrypt_message(plain_text_user_id))
        if not login_set:
            #login not found
            return False
        else:
            return self.get_hashed_password(plain_text_password) == login_set['password']
