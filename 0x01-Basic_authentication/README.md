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
bob@dylan:~$ pip3 install -r requirements.txt
...
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Serving Flask app "app" (lazy loading)
...
bob@dylan:~$
Use the API (in another tab or in your browser)
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
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
bob@dylan:~$
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
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized" -vvv
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
bob@dylan:~$
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
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden"
{
  "error": "Forbidden"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden" -vvv
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
bob@dylan:~$
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
bob@dylan:~$ cat main_0.py
#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())

bob@dylan:~$ 
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_0.py
False
None
None
bob@dylan:~$
```
   
### 4. Define which routes don't need authentication

Update the method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: in Auth that returns True if the path is not in the list of strings excluded_paths:

- [ ] Returns `True` if `path` is `None`
- [ ] Returns `True` if `excluded_paths` is `None` or empty
- [ ] Returns `False` if `path` is in `excluded_paths`
- [ ] You can assume `excluded_paths` contains `string` path always ending by a `/`
- [ ] This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must be returned `False` if `excluded_paths` contains `/api/v1/status/`
```bash
bob@dylan:~$ cat main_1.py
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

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_1.py
True
True
True
False
False
True
True
bob@dylan:~$
```

### 5. Request validation!

Now you will validate all requests to secure the API:

Update the method def authorization_header(self, request=None) -> str: in api/v1/auth/auth.py:

If request is None, returns None
If request doesn’t contain the header key Authorization, returns None
Otherwise, return the value of the header request Authorization
Update the file api/v1/app.py:

Create a variable auth initialized to None after the CORS definition
Based on the environment variable AUTH_TYPE, load and assign the right instance of authentication to auth
if auth:
import Auth from api.v1.auth.auth
create an instance of Auth and assign it to the variable auth
Now the biggest piece is the filtering of each request. For that you will use the Flask method before_request

Add a method in api/v1/app.py to handler before_request
if auth is None, do nothing
if request.path is not part of this list ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'], do nothing - you must use the method require_auth from the auth instance
if auth.authorization_header(request) returns None, raise the error 401 - you must use abort
if auth.current_user(request) returns None, raise the error 403 - you must use abort
In the first terminal:
```bash
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

### 6. Basic auth

Create a class BasicAuth that inherits from Auth. For the moment this class will be empty.

Update api/v1/app.py for using BasicAuth class instead of Auth depending of the value of the environment variable AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:

import BasicAuth from api.v1.auth.basic_auth
create an instance of BasicAuth and assign it to the variable auth
Otherwise, keep the previous mechanism with auth an instance of Auth.

In the first terminal:
```bash
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```