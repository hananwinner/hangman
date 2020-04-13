from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

users = {
    'unbotify': 'unbotify',
    'john': 'spider'
}


def check_basicAuth(username, password, required_scopes):
    if username in users:
        if password == users[username]:
            return {'test_key': 'test_value'}
    return False


