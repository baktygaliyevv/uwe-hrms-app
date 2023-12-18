import hashlib

def hash_password(password, salt):
    combined_string = password.encode('utf-8') + salt.encode('utf-8')
    hashed_password = hashlib.sha256(combined_string).hexdigest()
    return hashed_password