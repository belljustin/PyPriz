from os import urandom

from pypriz.models.token import Token

def generate_token(ip_address):
    token_secret = urandom(24)
    token = Token(ip_address, token_secret)
    return token

def validate_token():
    pass
