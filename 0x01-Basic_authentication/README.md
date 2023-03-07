# 0x01. Basic authentication

Background Context
In this project, i learnt what the authentication process means and implement a **Basic Authentication** on a simple API.

In the industry, you should not implement your own Basic authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

![](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/5/6ccb363443a8f301bc2bc38d7a08e9650117de7c.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20230307%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230307T155410Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=6f38745b596c68b1670799449cdd2bcea9559e9d7b7663d73e2362e9c4de9684)



## Tasks
### 0. Simple-basic-API

In this repo, you will find a simple API with one model: User. Storage of these users is done via a serialization/deserialization in files.

Setup and start server
```bash
user@ubuntu:~$ pip3 install -r requirements.txt
...
user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Serving Flask app "app" (lazy loading)
...
user@ubuntu:~$
Use the API (in another tab or in your browser)
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/status HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 16
< Access-Control-Allow-Origin: *
< Server: Werkzeug/1.0.1 Python/3.7.5
< Date: Mon, 18 May 2020 20:29:21 GMT
< 
{"status":"OK"}
* Closing connection 0
user@ubuntu:~$
```
   
### 1. Error handler: Unauthorized

What the HTTP status code for a request unauthorized? `401` of course!

Edit [api/v1/app.py](./api/v1/app.py):

- [x] Add a new error handler for this status code, the response must be:
    - [x] a JSON: `{"error": "Unauthorized"}`
    - [x] status code `401`
    - [x] you must use `jsonify` from `Flask`
For testing this new error handler, 

add a new endpoint in [api/v1/views/index.py](./api/v1/views/index.py):

- [x] Route: GET `/api/v1/unauthorized`
- [x] This endpoint must raise a 401 error by using `abort` - [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)
By calling `abort(401)`, the error handler for 401 will be executed.

In the first terminal:
```bash
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized"
{
  "error": "Unauthorized"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/unauthorized HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:50:40 GMT
< 
{
  "error": "Unauthorized"
}
* Closing connection 0
user@ubuntu:~$
```
### 2. Error handler: Forbidden

What the HTTP status code for a request where the user is authenticate but not allowed to access to a resource? `403` of course!

Edit [api/v1/app.py](./api/v1/app.py):

- [x] Add a new error handler for this status code, the response must be:
    - [x] a JSON: `{"error": "Forbidden"}`
    - [x] status code `403`
    - [x] you must use `jsonify` from Flask

For testing this new error handler, add a new endpoint in [api/v1/views/index.py](./api/v1/views/index.py):

- [x] Route: GET `/api/v1/forbidden`
- [x] This endpoint must raise a `403` error by using abort - Custom Error Pages
By calling `abort(403)`, the error handler for `403` will be executed.

In the first terminal:
```bash
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/forbidden"
{
  "error": "Forbidden"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/forbidden" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/forbidden HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:54:22 GMT
< 
{
  "error": "Forbidden"
}
* Closing connection 0
user@ubuntu:~$
```

### 3. Auth class

Now you will create a class to manage the API authentication.

- [x] Create a folder [api/v1/auth](./api/v1/auth)
- [x] Create an empty file [api/v1/auth/__init__.py](./api/v1/auth/__init__.py)
- [x] Create the class Auth:
    - [x] in the file [api/v1/auth/auth.py](./api/v1/auth/auth.py)
    - [x] import `request` from `flask`
    - [x] class name `Auth`
    - [x] public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - `path` and `excluded_paths` will be used later, now, you don’t need to take care of them
    - [x] public method `def authorization_header(self, request=None) -> str:` that returns `None` - request will be the Flask `request `object
    - [x] public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - request will be the Flask r`equest` object
This class is the template for all authentication system you will implement.

```bash
user@ubuntu:~$ cat main_0.py
#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())

user@ubuntu:~$ 
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_0.py
False
None
None
user@ubuntu:~$
```
   
### 4. Define which routes don't need authentication

Update the method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: in Auth that returns True if the path is not in the list of strings excluded_paths:

- [x] Returns `True` if `path` is `None`
- [x] Returns `True` if `excluded_paths` is `None` or empty
- [x] Returns `False` if `path` is in `excluded_paths`
- [x] You can assume `excluded_paths` contains `string` path always ending by a `/`
- [x] This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must be returned `False` if `excluded_paths` contains `/api/v1/status/`
```bash
user@ubuntu:~$ cat main_1.py
#!/usr/bin/env python3
""" Main 1
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth(None, None))
print(a.require_auth(None, []))
print(a.require_auth("/api/v1/status/", []))
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_1.py
True
True
True
False
False
True
True
user@ubuntu:~$
```

### 5. Request validation!

Now you will validate all requests to secure the API:

Update the method `def authorization_header(self, request=None) -> str: in api/v1/auth/auth.py:`

- [x] If `request` is `None`, returns `None`
- [x] If `request` doesn’t contain the header key `Authorization`, returns `None`
- [x] Otherwise, return the value of the header request `Authorization`

Update the file [api/v1/app.py](./api/v1/app.py):

- [x] Create a variable `auth` initialized to `None` after the `CORS` definition
- [x] Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`
    - [x] if `auth`:
        - [x] import `Auth` from `api.v1.auth.auth`
        - [x] create an instance of `Auth` and assign it to the variable `auth`

Now the biggest piece is the filtering of each request. For that you will use the Flask method before_request

- [x] Add a method in [api/v1/app.py](./api/v1/app.py) to handler `before_request`
    - [x] if `auth` is `None`, do nothing
    - [x] if `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`, do nothing - you must use the method `require_auth` from the `auth` instance
    - [x] if `auth.authorization_header(request)` returns `None`, raise the `error 401` - you must use `abort`
    - [x] if `auth.current_user(request)` returns `None`, raise the `error 403` - you must use `abort`
    
In the first terminal:
```bash
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
user@ubuntu:~$ 
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
user@ubuntu:~$ 
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
user@ubuntu:~$
```

### 6. Basic auth

Create a class `BasicAuth` that inherits from `Auth`. For the moment this class will be empty.

Update [api/v1/app.py](./api/v1/app.py) for using `BasicAuth` class instead of `Auth` depending of the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `basic_auth`:

- [x] import BasicAuth from [api.v1.auth.basic_auth](./api.v1.auth.basic_auth)
- [x] create an instance of `BasicAuth` and assign it to the variable a`uth`

Otherwise, keep the previous mechanism with `auth` an instance of `Auth`.

In the first terminal:
```bash
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
user@ubuntu:~$
```

### 7. Basic - Base64 part

Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` that returns the `Base64` part of the `Authorization` header for a `Basic Authentication:`

- [x] Return `None` if `authorization_header `is `None`
- [x] Return `None` if `authorization_header` is not a string
- [x] Return `None` if `authorization_header` doesn’t start by Basic (with a space at the end)
- [x] Otherwise, return the value after `Basic` (after the space)
- [x] You can assume `authorization_header` contains only one `Basic`
```bash
user@ubuntu:~$ cat main_2.py
#!/usr/bin/env python3
""" Main 2
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("Holberton School"))
print(a.extract_base64_authorization_header("Basic Holberton"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(a.extract_base64_authorization_header("Basic1234"))

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_2.py
None
None
None
Holberton
SG9sYmVydG9u
SG9sYmVydG9uIFNjaG9vbA==
None
user@ubuntu:~$
```

### 8. Basic - Base64 decode

Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` that returns the decoded value of a `Base64` string `base64_authorization_header:`

- [x] Return `None` if `base64_authorization_header` is `None`
- [x] Return `None` if `base64_authorization_header` is not a `string`
- [x] Return `None` if `base64_authorization_header` is not a `valid Base64` - you can use `try/except`
- [x] Otherwise, return the decoded value as `UTF8` string - you can use `decode('utf-8')`
```bash
user@ubuntu:~$ cat main_3.py
#!/usr/bin/env python3
""" Main 3
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.decode_base64_authorization_header(None))
print(a.decode_base64_authorization_header(89))
print(a.decode_base64_authorization_header("Holberton School"))
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_3.py
None
None
None
Holberton
Holberton School
Holberton School
user@ubuntu:~$
```
   
### 9. Basic - User credentials

Add the method `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in the class `BasicAuth` that returns the user `email` and `password` from the `Base64` decoded value.

This method must return 2 values
- [x] Return `None`, `None` if `decoded_base64_authorization_header` is `None`
- [x] Return `None`, `None` if `decoded_base64_authorization_header` is not a `string`
- [x] Return `None`, `None` if `decoded_base64_authorization_header` doesn’t contain `:`
- [x] Otherwise, return the user `email` and the user `password` - these 2 values must be separated by a `:`
You can assume `decoded_base64_authorization_header` will contain only one :
```bash
user@ubuntu:~$ cat main_4.py
#!/usr/bin/env python3
""" Main 4
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_user_credentials(None))
print(a.extract_user_credentials(89))
print(a.extract_user_credentials("Holberton School"))
print(a.extract_user_credentials("Holberton:School"))
print(a.extract_user_credentials("bob@gmail.com:toto1234"))

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_4.py
(None, None)
(None, None)
(None, None)
('Holberton', 'School')
('bob@gmail.com', 'toto1234')
user@ubuntu:~$
```

### 10. Basic - User object

Add the method def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'): in the class BasicAuth that returns the User instance based on his email and password.

- [x] Return `None` if `user_email` is `None`or not a `string`
- [x] Return `None` if `user_pwd` is `None` or not a `string`
- [x] Return `None` if your database (file) doesn’t contain any `User` instance with `email`equal to `user_email` - you should use the class method search of the `User` to lookup the list of users based on their `email`. Don’t forget to test all cases: “what if there is no user in DB?”, etc.
- [x] Return `None` if `user_pwd `is not the `password` of the User instance found - you must use the method `is_valid_password` of User
- [x] Otherwise, return the User instance
```bash
user@ubuntu:~$ cat main_5.py
#!/usr/bin/env python3
""" Main 5
"""
import uuid
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Bob"
user.last_name = "Dylan"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()

""" Retreive this user via the class BasicAuth """

a = BasicAuth()

u = a.user_object_from_credentials(None, None)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(89, 98)
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials("email@notfound.com", "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, "pwd")
print(u.display_name() if u is not None else "None")

u = a.user_object_from_credentials(user_email, user_clear_pwd)
print(u.display_name() if u is not None else "None")

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_5.py 
New user: Bob Dylan
None
None
None
None
Bob Dylan
user@ubuntu:~$
```

### 11. Basic - Overload current_user - and BOOM!

Now, you have all pieces for having a complete Basic authentication.

Add the method `def current_user(self, request=None) -> TypeVar('User')` in the class `BasicAuth` that overloads `Auth` and retrieves the `User` instance for a request:

- [x] You must use `authorization_header`
- [x] You must use `extract_base64_authorization_header`
- [x] You must use `decode_base64_authorization_header`
- [x] You must use `extract_user_credentials`
- [x] You must use `user_object_from_credentials`

With this update, now your API is fully protected by a Basic Authentication. Enjoy!

In the first terminal:
```bash
user@ubuntu:~$ cat main_6.py
#!/usr/bin/env python3
""" Main 6
"""
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"
user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {} / {}".format(user.id, user.display_name()))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))

user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_6.py 
New user: 9375973a-68c7-46aa-b135-29f79e837495 / bob@hbtn.io
Basic Base64: Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh
user@ubuntu:~$
user@ubuntu:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In a second terminal:
```bash
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
user@ubuntu:~$ 
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
user@ubuntu:~$ 
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
user@ubuntu:~$ 
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic test"
{
  "error": "Forbidden"
}
user@ubuntu:~$
user@ubuntu:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh"
[
  {
    "created_at": "2017-09-25 01:55:17", 
    "email": "bob@hbtn.io", 
    "first_name": null, 
    "id": "9375973a-68c7-46aa-b135-29f79e837495", 
    "last_name": null, 
    "updated_at": "2017-09-25 01:55:17"
  }
]
user@ubuntu:~$ 
```