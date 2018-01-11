from behave import *
import sys
import flask

# These steps are for requirements testing.

@given('we have python 3 installed')
def python_test(context):
	#Make sure python 3 is being run. I don't think behave works on python 2,
	#but better safe than sorry. This also verifies behave was installed.
    assert sys.version_info[0] is 3

@given('we have Flask installed')
def flask_test(context):
	#Make sure Flask has correctly been installed. This is just passed, since
	#this python file won't run at all if flask hasn't been installed.
	pass

@then('behave will pass this test')
def pass_test(context):
    #Make sure a test didn't fail for a reason that behave didn't normally
	#catch. This isn't useful here, but is more useful in complex testing
	#states.
	assert context.failed is False

# Test to be sure the server is running.

@given('the client is running')
def client_check(context):
    assert context.api is not False