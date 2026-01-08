"""Simple, simulated LLM scenario generator.

This module does NOT call any real LLM APIs. It only
returns fixed BDD-style scenarios based on the input
requirement text. The goal is to demonstrate how an
LLM *could* be used in a controlled way for BDD.
"""

from typing import List


def generate_scenarios(requirement_text: str) -> List[str]:
	"""Generate BDD scenarios from a plain-English requirement.

	For this demo, we simulate LLM behaviour with simple
	rule-based logic:

	- If the requirement mentions "login" (case-insensitive),
	  we return one happy-path and one negative scenario.
	- Otherwise, we return an empty list.

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


if __name__ == "__main__":  # simple manual demo helper
	sample_requirement = "Users must be able to login using a username and password."
	for block in generate_scenarios(sample_requirement):
		print(block)
		print("-" * 40)

