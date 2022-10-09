```python
import pandas as pd
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
```


```python
#Using a DataFrame to emulate a table of users
import pandas as pd
userdata = {
    "id": [1,2,3,4,5],
    "name": ["Taylor","Tyler","Alice","Bob","Eve"],
    "score": [99, 73, 65, 50, 77]    
}

userdf = pd.DataFrame(userdata)

toprow = userdf['score'].idxmax()
top = userdf.iloc[toprow]
top['score']
```




    99




```python
app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "Taylor": generate_password_hash("password"),
    "Admin": generate_password_hash("securepassword"),
    "Alice": generate_password_hash("ecilA"),
    "Bob": generate_password_hash("boB")
    
}

userroles = {
    "Taylor": "user",
    "Admin": "admin",
    "Alice": "user",
    "Bob": "user"
}

def get_roles(user):
    list = []
    role = userroles[user]
    list.append(role)
    return list

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    
@auth.get_user_roles
def get_user_roles(user):
    roles = get_roles(user)    
    return roles

@app.route('/')
def index():
    return "The current high score is {} and held by {}".format(top['score'], top['name'])

@app.route('/user')
@auth.login_required
def user():
    row = userdf.loc[userdf['name'] == auth.current_user()]
    return "Hello, {}! Your current high score is {}".format(auth.current_user(), row['score'].values[0])

@app.route('/scores')
@auth.login_required(role='admin')
def scores():
    return userdf.to_json()

if __name__ == '__main__':
    app.run()
```

     * Serving Flask app "__main__" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
    

     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    127.0.0.1 - - [09/Oct/2022 14:43:54] "[37mGET / HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:43:55] "[33mGET /favicon.ico HTTP/1.1[0m" 404 -
    127.0.0.1 - - [09/Oct/2022 14:44:00] "[37mGET /user HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:44:04] "[31m[1mGET /scores HTTP/1.1[0m" 403 -
    127.0.0.1 - - [09/Oct/2022 14:44:09] "[37mGET /scores HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:44:19] "[37mGET / HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:44:26] "[37mGET /user HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:44:31] "[37mGET /user HTTP/1.1[0m" 200 -
    127.0.0.1 - - [09/Oct/2022 14:44:36] "[31m[1mGET /user HTTP/1.1[0m" 401 -
    127.0.0.1 - - [09/Oct/2022 14:44:42] "[37mGET /scores HTTP/1.1[0m" 200 -
    


```python

```
