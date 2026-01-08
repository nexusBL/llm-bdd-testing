"""BDD step definitions for the happy-path login scenario.

This uses pytest-bdd for the BDD glue and the
pytest-playwright plugin for browser automation.
Only the approved happy path scenario is automated.
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from threading import Thread

import pytest
from playwright.sync_api import Page
from pytest_bdd import given, scenario, then, when


@scenario("../features/login.feature", "Valid user logs in successfully")
def test_valid_user_logs_in_successfully():
	"""End-to-end test for a valid login."""


@pytest.fixture(scope="session")
def app_url() -> str:
	"""Return an HTTP URL that serves sample_app.html locally.

	This keeps the demo local while avoiding browser
	restrictions around the file:// scheme.
	"""

	root_dir = Path(__file__).resolve().parents[1] / "app"
	handler = partial(SimpleHTTPRequestHandler, directory=str(root_dir))
	with TCPServer(("127.0.0.1", 0), handler) as httpd:
		port = httpd.server_address[1]
		server_thread = Thread(target=httpd.serve_forever, daemon=True)
		server_thread.start()
		try:
			yield f"http://127.0.0.1:{port}/sample_app.html"
		finally:
			httpd.shutdown()
			server_thread.join()


@given("the user is on the login page")
def open_login_page(page: Page, app_url: str) -> None:
	page.goto(app_url)


@when("the user enters valid credentials")
def enter_valid_credentials(page: Page) -> None:
	page.fill("#username", "admin")
	page.fill("#password", "admin123")


@when("the user clicks the Login button")
def click_login(page: Page) -> None:
	page.click("#login")


@then("the user is redirected to the dashboard")
def redirected_to_dashboard(page: Page) -> None:
	# We only care that the browser navigates to a URL
	# ending in "dashboard.html". The destination page
	# itself is not part of this simple demo.
	assert page.url.endswith("dashboard.html")

