"""Simple, simulated LLM scenario generator.

This module does not call any real LLM APIs. It just
returns fixed BDD-style scenarios from the input
requirement text to show how an LLM *could* be plugged
into a BDD-style workflow in a controlled way.
"""

from typing import List


def generate_scenarios(requirement_text: str) -> List[str]:
	"""Generate BDD scenarios from a plain-English requirement.

	For this demo, the "LLM" is just a small set of
	rules:

	- If the requirement mentions "login" (case-insensitive),
	  return one happy-path and one negative scenario.
	- Otherwise, return an empty list.

	Scenarios are returned as plain-text Gherkin blocks.
	"""

	if not isinstance(requirement_text, str):
		raise TypeError("requirement_text must be a string")

	text = requirement_text.lower()
	scenarios: List[str] = []

	if "login" in text:
		happy_path = """Feature: User login

  Scenario: Valid user logs in successfully
	Given the user is on the login page
	When the user enters valid credentials
	And the user clicks the Login button
	Then the user is redirected to the dashboard
""".rstrip()

		negative_path = """Feature: User login

  Scenario: Invalid user cannot log in
	Given the user is on the login page
	When the user enters invalid credentials
	And the user clicks the Login button
	Then an error message is displayed
""".rstrip()

		scenarios.append(happy_path)
		scenarios.append(negative_path)

	return scenarios



if __name__ == "__main__":  # quick manual demo helper
	sample_requirement = "Users must be able to login using a username and password."
	for block in generate_scenarios(sample_requirement):
		print(block)
		print("-" * 40)

