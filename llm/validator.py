"""Very simple scenario validator for known actions.

This module acts as a small safety check. It looks at
BDD scenarios before they are used for automation and
only accepts steps that use a short, known set of
actions. This keeps behaviour predictable and easy to
review.
"""

from typing import Iterable


# Action keywords that are treated as safe/known
KNOWN_ACTION_KEYWORDS = {"login", "enters", "clicks", "redirected", "displayed"}


def _extract_step_text(line: str) -> str:
	"""Return the text part of a step after Given/When/Then/And.

	Lines that are not step definitions are returned unchanged.
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

	The check is intentionally simple: it just looks for at
	least one of the known action keywords in the text.
	"""

	text = step_text.lower()

	if not any(keyword in text for keyword in KNOWN_ACTION_KEYWORDS):
		return False

	return True


def validate_scenarios(scenarios: Iterable[str]) -> bool:
	"""Return True if all scenarios use only known actions.

	Every step line in every scenario must contain at least one
	of the allowed action keywords. If any step fails that
	check, validation fails for the whole set.
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


if __name__ == "__main__":  # quick manual check helper
	from llm.scenario_generator import generate_scenarios

	req = "Users must be able to login using a username and password."
	blocks = generate_scenarios(req)
	print("Validation result:", validate_scenarios(blocks))

