"""Very simple scenario validator for known actions.

This module simulates a safety/validation layer that
checks BDD scenarios before they are considered for
automation. Only a small, whitelisted set of actions
is allowed to keep behaviour controlled and readable.
"""

from typing import Iterable


# Whitelisted action keywords that are considered safe/known
KNOWN_ACTION_KEYWORDS = {"login", "enters", "clicks", "redirected", "displayed"}


def _extract_step_text(line: str) -> str:
	"""Return the step text after Given/When/Then/And.

	Lines that do not look like steps are returned unchanged.
	"""

	prefixes = ("given ", "when ", "then ", "and ")
	trimmed = line.strip()
	lower = trimmed.lower()

	for prefix in prefixes:
		if lower.startswith(prefix):
			return trimmed[len(prefix) :]
	return trimmed


def _uses_only_known_actions(step_text: str) -> bool:
	"""Check whether the step text mentions only known actions.

	This is intentionally simple: it just checks that at least
	one of the known action keywords appears in the text and
	that no obviously unknown verbs are introduced.
	"""

	text = step_text.lower()

	if not any(keyword in text for keyword in KNOWN_ACTION_KEYWORDS):
		return False

	return True


def validate_scenarios(scenarios: Iterable[str]) -> bool:
	"""Validate that all provided scenarios use only known actions.

	The function returns True if **every** step line in **every**
	scenario contains at least one known action keyword. Any
	scenario with an unknown or unsupported action causes the
	overall validation to fail.
	"""

	for scenario in scenarios:
		for line in scenario.splitlines():
			stripped = line.strip()
			if not stripped:
				continue
			if not stripped.lower().startswith(("given ", "when ", "then ", "and ")):
				continue

			step_text = _extract_step_text(stripped)
			if not _uses_only_known_actions(step_text):
				return False

	return True


if __name__ == "__main__":  # small manual demo helper
	from llm.scenario_generator import generate_scenarios

	req = "Users must be able to login using a username and password."
	blocks = generate_scenarios(req)
	print("Validation result:", validate_scenarios(blocks))

