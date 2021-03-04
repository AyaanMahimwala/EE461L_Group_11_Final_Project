import hashlib
import base64
import bcrypt

from ..db_entry import DataSet
from ..mongo import MongoEntry
from .login_cred_schema import LoginSetSchema

SALT_ROUNDS = 16

class LoginSetService(object):
    """
    Called on init, sets the client which is an abstract 'DataSet' on the frontend
    and a mongodb entry on the backend. It also sets the 'user_id' and 'password' 
    so that we can save user specific logins.
    """
    def __init__(self, user_id, password, login_set_client=DataSet(adapter=MongoEntry)):
        self.login_set_client = login_set_client
        self.user_id = user_id
        if not user_id:
            raise Exception("user id not provided")
        self.password = password
        if not password:
            raise Exception("password not provided")

    def get_hashed_password(plain_text_password):
      # Hash a password for the first time
      # Using bcrypt, the salt is saved into the hash itself preventing rainbow table attacks
      # We use sha256 and encode using baase 64 to bypass the max length problems of blowfish
      return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), bcrypt.gensalt(rounds = SALT_ROUNDS))

    def check_password(plain_text_password, hashed_password):
      # Check hashed password. Using bcrypt, the salt is saved into the hash itself
      return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), hashed_password)
