# 0x00. Personal data

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/5c48d4f6d4dd8081eb48.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20230302%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230302T142536Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=aa9950baef76e5e55bfdceb91de3e2dc2b65e59aa5fff66f7d0f2ed44a085116)


## Tasks
### [0. Regex-ing](./filtered_logger.py)

Write a function called `filter_datum` that returns the log message obfuscated:

- Arguments:
    - [x] `fields`: a list of strings representing all fields to obfuscate
    - [x] `redaction`: a string representing by what the field will be obfuscated
    - [x] `message`: a string representing the log line
    - [x] `separator`: a string representing by which character is separating all fields in the log line (message)
- [x] The function should use a regex to replace occurrences of certain field values.
- [x] `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.
```bash
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

bob@dylan:~$
bob@dylan:~$ ./main.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
bob@dylan:~$
```


### [1. Log formatter](./filtered_logger.py)

Copy the following code into `filtered_logger.py`.
```py
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
```
Update the class to accept a list of strings `fields` constructor argument.

Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for `fields` in fields should be filtered.

DO NOT extrapolate `FORMAT` manually. The `format` method should be less than 5 lines long.
```bash
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

import logging
import re

RedactingFormatter = __import__('filtered_logger').RedactingFormatter

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))

bob@dylan:~$
bob@dylan:~$ ./main.py
[HOLBERTON] my_logger INFO 2019-11-19 18:24:25,105: name=Bob; email=***; ssn=***; password=***;
bob@dylan:~$
```