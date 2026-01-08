## LLM-Assisted BDD Functional Testing for a Sample Web Application

This repository is a **small case study** built for campus hiring. It
shows how LLM-style behaviour *could* support BDD-style functional
testing, while still keeping everything simple, safe, and easy to
explain.

> Note: No real LLM APIs are used. All behaviour is simulated with
> straightforward Python code.

### Objective

- Start from plain-English requirements and turn them into BDD
	scenarios.
- Add a simple validation step so only known, safe actions are used.
- Require a human approval step before any scenario is automated.
- Run automation only for the approved happy-path scenario using
	Playwright.

### Workflow

1. **Requirement**  
	 A short business requirement like "Users must be able to login" is
	 written in plain English.

2. **Scenario generation (`llm/scenario_generator.py`)**  
	 - `generate_scenarios(requirement_text)` acts like a very small,
		 rule-based LLM.  
	 - If the text mentions "login", it returns **one happy path** and
		 **one negative** scenario in Gherkin format.  
	 - Otherwise, it returns no scenarios. No APIs, LangChain, or
		 embeddings are involved.

3. **Validation (`llm/validator.py`)**  
	 - `validate_scenarios(scenarios)` checks that each step line only
		 uses a short list of allowed actions: `login`, `enters`, `clicks`,
		 `redirected`, `displayed`.  
	 - If any step does not use at least one of these actions, the
		 scenarios are treated as not valid for automation.

4. **Manual approval (`approval/approval.json`)**  
	 - A QA reviewer marks **only** the happy-path scenario
		 "Valid user logs in successfully" as approved.  
	 - Negative or exploratory flows are kept for analysis, not for
		 automation.

5. **Selected scenarios for automation (`features/login.feature`)**  
	 - This feature file holds just one scenario: the approved happy
		 path.  
	 - It uses clear Given–When–Then steps and points to the local login
		 page in `app/sample_app.html`.

6. **Automated execution (`tests/test_login_steps.py`)**  
	 - Uses **pytest-bdd** for the BDD layer and **Playwright** (through
		 `pytest-playwright`) for the browser.  
	 - Opens the local login page, enters the approved
		 credentials (`admin` / `admin123`), clicks **Login**, and checks
		 that the browser navigates to a URL ending in `dashboard.html`.  
	 - Only the approved happy-path scenario is wired into automation.

7. **Reporting (`reports/execution_report.txt`)**  
	 - Stores a short test summary: scenario name, validation status,
		 manual approval status, and final execution result.  
	 - This file is easy to show in an interview or slide deck.

### Sample Application (`app/sample_app.html`)

The sample app is a very small HTML page with:

- A username textbox
- A password textbox
- A **Login** button

The behaviour is straightforward:

- If `username == "admin"` and `password == "admin123"`, the browser
	is redirected to `dashboard.html`.
- For any other combination, the page displays "Invalid credentials".

No extra pages or frameworks are used.

### Safety and Control Principles

- **Not for production:** This project is for learning and campus
	hiring discussions only.
- **No real LLM calls:** All "LLM" behaviour is local and
	deterministic.
- **No advanced AI stack:** No embeddings, vector databases, or extra
	orchestration layers.
- **Human in the loop:** Only validated and manually approved scenarios
	can be automated.
- **Clear separation of responsibilities:**
	- Scenario generation in `llm/`
	- Validation in `llm/`
	- Human approval in `approval/`
	- Executable BDD in `features/`
	- Automation code in `tests/`
	- Summary and reporting in `reports/`

### How to Run the Demo (locally)

1. Install dependencies (from the repo root):

	 ```powershell
	 pip install -r requirements.txt
	 playwright install
	 ```

2. Run the automated BDD test:

	 ```powershell
	 pytest -q
	 ```

The goal of this setup is to stay small and readable so a reviewer can
quickly understand the flow and reasoning during an interview.

