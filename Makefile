.PHONY: install install-api install-web test test-api test-web smoke clean allure-api allure-web

install: install-api install-web

install-api:
	cd api && pip install -r requirements.txt

install-web:
	cd web && pip install -r requirements.txt

test: test-api test-web

test-api:
	cd api && pytest

test-web:
	cd web && pytest

smoke:
	cd api && pytest -m smoke
	cd web && pytest -m smoke

allure-api:
	cd api && allure serve allure-results

allure-web:
	cd web && allure serve allure-results

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name allure-results -exec rm -rf {} +
	find . -type d -name allure-report -exec rm -rf {} +
	find . -type d -name screenshots -exec rm -rf {} +
