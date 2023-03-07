#!/usr/bin/env python3
'''Authentication module
'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''User Authentication class
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Ensures authentication is required
        '''
        return

    def authorization_header(self, request=None) -> str:
        '''includes authorization header to http req
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Retrieves the current users
        '''
        return None
