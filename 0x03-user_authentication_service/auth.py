#!/usr/bin/env python3
'''user authentication module
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''Hashe and encrypt a password.
    '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    '''Auth class to interact with the authentication database.
    '''

    def __init__(self):
        '''constructor method
        '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Adds a new user to the database.
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''Checks if a user's login details are valid.
        '''
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False
