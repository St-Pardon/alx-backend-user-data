# 0x03. User authentication service

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2019/12/4cb3c8c607afc1d1582d.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20230313%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230313T162546Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=88fb1f05ffa2f38bcb30ca7daa29f9105b594c48ca4ba46985c0cae0acd4456c)

## Setup
You will need to install `bcrypt`
```sh
pip3 install bcrypt
```


## Tasks
### User model
mandatory
In this task you will create a SQLAlchemy model named `User` for a database table named `users` (by using the [mapping declaration]() of SQLAlchemy).

The model will have the following attributes:

- [ ] `id`, the integer primary key
- [ ] `email`, a non-nullable string
- [ ] `hashed_password`, a non-nullable string
- [ ] `session_id`, a nullable string
- [ ] `reset_token`, a nullable string
```sh
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

bob@dylan:~$ python3 main.py
users
users.id: INTEGER
users.email: VARCHAR(250)
users.hashed_password: VARCHAR(250)
users.session_id: VARCHAR(250)
users.reset_token: VARCHAR(250)
bob@dylan:~$ 
```