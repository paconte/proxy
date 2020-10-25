""" The class contains jwt utils to generate a jwt header"""
import uuid
from datetime import datetime
import jwt


def encode(payload, key, algo):
    """encodes the argument payload with the given key and algorithm"""
    return jwt.encode(payload, key, algorithm=algo)


def decode(encoded, key, algo):
    """decodes the argument payload with the given key and algorithm"""
    return jwt.decode(encoded, key, algorithms=algo)


def get_default_payload(user='username'):
    """returns the payload from the specification"""
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%d')
    jti = uuid.uuid4()
    return {'user': user, 'date': date, 'iat': now, 'jti': jti.hex}


def get_default_jwt(key, algo, user='username'):
    """returns the jwt header content from the specification"""
    payload = get_default_payload(user)
    return encode(payload, key=key, algo=algo)
