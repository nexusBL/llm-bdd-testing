## LLM-Assisted BDD Functional Testing for a Sample Web Application

This repository is a **controlled, campus-hiring case study** that
demonstrates how Large Language Models (LLMs) *could* assist BDD-style
functional testing, while keeping safety, validation, and human control
at the center.

> Important: No real LLM APIs are called. All behaviour is simulated
> with simple, readable Python logic.

### Objective

- Show how plain-English requirements can be turned into BDD scenarios.
- Enforce a validation layer that only allows known, safe actions.
- Require explicit human approval before anything is automated.
- Automate **only** the approved happy-path scenario with Playwright.

### Workflow

1. **Requirement**  
	 A business requirement such as "Users must be able to login" is
	 provided as plain text.

2. **Scenario generation (`llm/scenario_generator.py`)**  
	 - `generate_scenarios(requirement_text)` simulates an LLM:  
		 - If the text mentions "login", it returns **one happy path** and
			 **one negative** BDD scenario in Gherkin syntax.  
		 - Otherwise it returns no scenarios.  
	 - No APIs, no LangChain, no embeddings—just deterministic logic.

3. **Validation (`llm/validator.py`)**  
	 - `validate_scenarios(scenarios)` checks that each step line only
		 uses a small whitelist of known actions: `login`, `enters`,
		 `clicks`, `redirected`, `displayed`.  
	 - If any step uses unknown actions, validation fails.  
	 - This models a **safety gate** in front of automation.

4. **Manual approval (`approval/approval.json`)**  
	 - A QA reviewer explicitly approves **only** the happy-path
		 scenario: "Valid user logs in successfully".  
	 - Negative or exploratory scenarios are **not** approved for
		 automation and therefore are not present in the feature file.

5. **Selected scenarios for automation (`features/login.feature`)**  
	 - This feature file contains just one scenario: the approved
		 happy path.  
	 - It uses clean Given–When–Then syntax and maps directly to the
		 local login page in `app/sample_app.html`.

6. **Automated execution (`tests/test_login_steps.py`)**  
	 - Uses **pytest-bdd** for BDD glue and **Playwright** (via
		 `pytest-playwright`) for browser automation.  
	 - Opens the local `sample_app.html` over a `file:///` URL, enters
		 the approved credentials (`admin`/`admin123`), clicks **Login**, and
		 asserts that the browser navigates to a URL ending with
		 `dashboard.html`.  
	 - Only the approved happy-path scenario is automated.

7. **Reporting (`reports/execution_report.txt`)**  
	 - Captures a simple, readable summary: scenario name, validation
		 status, manual approval status, and execution result placeholder.  
	 - Suitable for screenshotting into slides as part of the case study.

### Sample Application (`app/sample_app.html`)

The sample app is a minimal HTML page with:

- A username field
- A password field
- A **Login** button

Logic is kept intentionally simple:

- If `username == "admin"` and `password == "admin123"`, the browser
	is redirected to `dashboard.html`.
- Otherwise, the page shows "Invalid credentials".

No additional pages or frameworks are used.

### Safety and Control Principles

- **No production usage:** This is a demo-only, campus-hiring case
	study.
- **No real LLM calls:** All "LLM" behaviour is deterministic and
	local.
- **No advanced AI logic:** No embeddings, vector stores, or external
	orchestration frameworks.
- **Human in the loop:** Automation is allowed only for scenarios that
	are validated and explicitly approved.
- **Separation of responsibilities:**
	- Scenario generation in `llm/`
	- Validation in `llm/`
	- Human approval in `approval/`
	- Executable BDD in `features/`
	- Automation code in `tests/`
	- Summary/reporting in `reports/`

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

This setup is intentionally minimal and aimed at being easy to read,
review, and present in a PPT deck during campus hiring discussions.

