Feature: Test to be sure everything is installed correctly

    Scenario: Test dependencies are installed correctly
        Given we have python 3 installed
        And we have Flask installed
		Then behave will pass this test