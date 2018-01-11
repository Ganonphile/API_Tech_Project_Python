Feature: GET performs properly

    Scenario: GET returns information as a json
    	Given the client is running
		When we GET a city from the client
		Then the information returned is a json