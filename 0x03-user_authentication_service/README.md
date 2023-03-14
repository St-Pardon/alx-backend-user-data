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

- [x] `id`, the integer primary key
- [x] `email`, a non-nullable string
- [x] `hashed_password`, a non-nullable string
- [x] `session_id`, a nullable string
- [x] `reset_token`, a nullable string
```sh
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

user@ubuntu:~$ python3 main.py
users
users.id: INTEGER
users.email: VARCHAR(250)
users.hashed_password: VARCHAR(250)
users.session_id: VARCHAR(250)
users.reset_token: VARCHAR(250)
user@ubuntu:~$ 
```

### 1. create user

In this task, you will complete the `DB` class provided below to implement the `add_user` method.
```py
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
```
Note that `DB._session`is a private property and hence should NEVER be used from outside the `DB` class.

Implement the `add_user` method, which has two required string arguments: `email` and `hashed_password`, and returns a `User` object. The method should save the `user` to the database. No validations are required at this stage.
```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

user@ubuntu:~$ python3 main.py
1
2
user@ubuntu:~$
```
   
### 2. Find user

In this task you will implement the `DB.find_user_by method`. This method takes in arbitrary keyword arguments and returns the first row found in the `users` table as filtered by the method’s input arguments. No validation of input arguments required at this point.

Make sure that SQLAlchemy’s `NoResultFound` and `InvalidRequestError` are raised when no results are found, or when wrong query arguments are passed, respectively.

**Warning:**

- [x] `NoResultFound` has been moved from `sqlalchemy.orm.exc` to `sqlalchemy.exc` between the version 1.3.x and 1.4.x of SQLAchemy - please make sure you are importing it from `sqlalchemy.orm.exc`
```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")        

user@ubuntu:~$ python3 main.py
1
1
Not found
Invalid
user@ubuntu:~$ 
```
   
### 3. update user

In this task, you will implement the `DB.update_user` method that takes as argument a required `user_id `integer and arbitrary keyword arguments, and returns `None`.

The method will use `find_user_by` to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.

If an argument that does not correspond to a user attribute is passed, raise a ValueError.

```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(user.id)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

user@ubuntu:~$ python3 main.py
1
Password updated
user@ubuntu:~$ 
```

### 4. Hash password

In this task you will define `a _hash_password `method that takes in a `password` string arguments and returns `bytes`.

The returned bytes is a salted hash of the input password, hashed with `bcrypt.hashpw`.
```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import _hash_password

print(_hash_password("Hello Holberton"))

user@ubuntu:~$ python3 main.py
b'$2b$12$eUDdeuBtrD41c8dXvzh95ehsWYCCAi4VH1JbESzgbgZT.eMMzi.G2'
user@ubuntu:~$
```
   
### 5. Register user

In this task, you will implement the `Auth.register_user` in the `Auth` class provided below:
```py
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
```
Note that `Auth._db` is a private property and should NEVER be used from outside the class.

`Auth.register_user` should take mandatory `email` and `password` string arguments and return a User object.

If a user already exist with the passed email, raise a `ValueError` with the message `User <user's email> already exists`.

If not, hash the password with `_hash_password`, save the user to the database using `self._db` and return the `User` object.
```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'me@me.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))        

user@ubuntu:~$ python3 main.py
successfully created a new user!
could not create a new user: User me@me.com already exists
user@ubuntu:~$
```
   
### 6. Basic Flask app

In this task, you will set up a basic Flask app.

Create a Flask app that has a single `GET` route (`"/"`) and use `flask.jsonify` to return a `JSON` payload of the form:
```py
{"message": "Bienvenue"}
```
Add the following code at the end of the module:
```py
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
```
   
### 7. Register user
In this task, you will implement the end-point to register a `user`. Define a `users` function that implements the `POST /users` route.

Import the `Auth` object and instantiate it at the root of the module as such:
```py
from auth import Auth


AUTH = Auth()
```
The end-point should expect two form data fields: `"email"` and `"password"`. If the user does not exist, the end-point should register it and respond with the following JSON payload:
```py
{"email": "<registered email>", "message": "user created"}
```
If the user is already registered, catch the exception and return a JSON payload of the form

{"message": "email already registered"}
and return a 400 status code

Remember that you should only use `AUTH` in this app. `DB` is a lower abstraction that is proxied by `Auth`.

Terminal 1:
```bash
user@ubuntu:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Terminal 2:
```bash
user@ubuntu:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 52
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:18 GMT
< 
{"email":"bob@me.com","message":"user created"}

user@ubuntu:~$
user@ubuntu:~$ curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /users HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 40
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 40 out of 40 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 400 BAD REQUEST
< Content-Type: application/json
< Content-Length: 39
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:03:33 GMT
< 
{"message":"email already registered"}
user@ubuntu:~$
```
   
### 8. Credentials validation

In this task, you will implement the `Auth.valid_login method`. It should expect `email` and `password` required arguments and return a boolean.

Try locating the user by `email`. If it exists, check the password with `bcrypt.checkpw`. If it matches return True. In any other case, return `False`.

```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

user@ubuntu:~$ python3 main.py
True
False
False
user@ubuntu:~$ 
```
   
### 9. Generate UUIDs

In this task you will implement a `_generate_uuid `function in the `auth` module. The function should return a string representation of a new `UUID.` Use the `uuid` module.

Note that the method is private to the `auth` module and should NOT be used outside of it.

   
### 10. Get session ID

In this task, you will implement the `Auth.create_session` method. It takes an `email` string argument and returns the session ID as a string.

The method should find the user corresponding to the email, generate a new `UUID` and store it in the database as the user’s `session_id`, then return the session ID.

Remember that only public methods of `self._db` can be used.
```bash
user@ubuntu:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

user@ubuntu:~$ python3 main.py
5a006849-343e-4a48-ba4e-bbd523fcca58
None
user@ubuntu:~$ 
```
   
### 11. Log in

In this task, you will implement a `login` function to respond to the `POST /sessions` route.

The request is expected to contain form data with `"email"` and a `"password"` fields.

If the login information is incorrect, use `flask.abort` to respond with a 401 HTTP status.

Otherwise, create a new session for the user, store it the session ID as a cookie with key "session_id" on the response and return a JSON payload of the form
```json
{"email": "<user email>", "message": "logged in"}
```
```sh
user@ubuntu:~$ curl -XPOST localhost:5000/users -d 'email=bob@bob.com' -d 'password=mySuperPwd'
{"email":"bob@bob.com","message":"user created"}
user@ubuntu:~$ 
user@ubuntu:~$  curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 37
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 37 out of 37 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 46
< Set-Cookie: session_id=163fe508-19a2-48ed-a7c8-d9c6e56fabd1; Path=/
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:34 GMT
< 
{"email":"bob@bob.com","message":"logged in"}
* Closing connection 0
user@ubuntu:~$ 
user@ubuntu:~$ curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=BlaBla' -v
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /sessions HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 34
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 34 out of 34 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: text/html; charset=utf-8
< Content-Length: 338
< Server: Werkzeug/1.0.1 Python/3.7.3
< Date: Wed, 19 Aug 2020 00:12:45 GMT
< 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
* Closing connection 0
user@ubuntu:~$ 
```