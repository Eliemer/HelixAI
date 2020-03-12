'''
This file will act as the main for the entire application.
It will dictate routes and call functions for the rest of
the application to work.
'''

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is the home page!'
