include .env

quality:
	uv run black .
	uv run isort .
	uv run flake8 .

tests:
	uv run pytest

tests-diarylab:
	uv run pytest tests/unit/diarylab --html=tests/htmlcov/diarylab.html

tests-secretbox:
	uv run pytest tests/unit/secretbox tests/integration/secretbox --html=tests/htmlcov/secretbox.html

tests-escapevault:
	uv run secretbox/tools/create_test_user.py
	uv run pytest tests/unit/test_escapevault_models.py tests/integration/escapevault --html=tests/htmlcov/escapevault.html

tests-sami:
	uv run pytest tests/unit/test_sami_models.py --html=tests/htmlcov/sami.html

tests-coverage:
	uv run pytest --cov=. tests --cov-report=html:tests/htmlcov

run:
	clear
	uv run manage.py runserver

deploy:
	uv pip freeze > requirements.txt
	rsync -a --exclude-from='.deployignore' . "$(DEPLOY_PATH)"
	cp secretbox.desktop ~/Bureau/
	cd "$(DEPLOY_PATH)"
	uv add -r requirements.txt
	uv run manage.py migrate

