#!/usr/bin/env python3
'''Authentication module
'''
from flask import request
from typing import List, TypeVar
import re


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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Retrieves the current users
        '''
        return None
