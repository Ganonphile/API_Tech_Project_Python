from flask import Flask
import api.api
import os

# The environment file serves as a way to control variables on a suite
# feature, or step level. In this case, we are using it as a way to implement
# a client for testing.

# Before_all tells behave to run this before doing anything else.
def before_all(context):
    context.api = Flask("api")