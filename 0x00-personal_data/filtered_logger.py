#!/usr/bin/env python3
'''personal data protection module
'''
import re
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    '''obfuscate log messages
    '''
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)
