Feature: User login

	# This feature file intentionally contains only the
	# approved happy path scenario. Negative paths are
	# kept for analysis and manual execution only.

	Scenario: Valid user logs in successfully
		Given the user is on the login page
		When the user enters valid credentials
		And the user clicks the Login button
		Then the user is redirected to the dashboard

