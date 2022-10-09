#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


# In[23]:


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


# In[26]:


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
    if username in users and             check_password_hash(users.get(username), password):
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


# In[ ]:




