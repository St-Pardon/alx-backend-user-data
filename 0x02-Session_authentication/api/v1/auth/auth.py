#!/usr/bin/env python3
'''Authentication module
'''
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    '''User Authentication class
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Ensures authentication is required
        '''
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        '''includes authorization header to http req
        '''
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Retrieves the current users
        '''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from request
        '''
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
