import hashlib
import base64
import bcrypt

SALT_ROUNDS = 16

def get_hashed_password(plain_text_password):
  # Hash a password for the first time
  # Using bcrypt, the salt is saved into the hash itself preventing rainbow table attacks
  # We use sha256 and encode using baase 64 to bypass the max length problems of blowfish
  return bcrypt.hashpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), bcrypt.gensalt(rounds = SALT_ROUNDS))

def check_password(plain_text_password, hashed_password):
  # Check hashed password. Using bcrypt, the salt is saved into the hash itself
  return bcrypt.checkpw(base64.b64encode(hashlib.sha256(plain_text_password).digest()), hashed_password)
