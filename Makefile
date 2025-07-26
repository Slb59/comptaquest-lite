include .env

quality:
	uv run isort .
	uv run black .
	uv run flake8 .

tests:
	uv run pytest
	npx playwright test

tests-diarylab:
	uv run pytest tests/unit/diarylab --html=tests/htmlcov/diarylab.html

tests-secretbox:
	uv run pytest tests/unit/secretbox tests/integration/secretbox --html=tests/htmlcov/secretbox.html

tests-escapevault:
	uv run manage.py create_test_user
	uv run pytest tests/unit/test_escapevault_models.py tests/integration/escapevault --html=tests/htmlcov/escapevault.html
	npx playwright test
	npx playwright show-report

tests-sami:
	uv run pytest tests/unit/test_sami_models.py --html=tests/htmlcov/sami.html

tests-coverage:
	uv run pytest --cov=. tests --cov-report=html:tests/htmlcov

run:
	clear
	uv run manage.py runserver

run-front:
	clear
	npm run build

run-test:
	clear
	cp db.sqlite3 db_test.sqlite3
	uv run manage.py reset_positions
	uv run manage.py runserver 8001 --settings=config.settings.test &
	sleep 3
	( \
		trap 'pkill -f runserver' EXIT; \
		npx playwright test \
	)

deploy:
	uv pip freeze > requirements.txt
	rsync -a --exclude-from='.deployignore' . "$(DEPLOY_PATH)"
	cp secretbox.desktop ~/Bureau/
	cd "$(DEPLOY_PATH)"
	uv add -r requirements.txt
	uv run manage.py migrate

dumpdata:
	uv run manage.py dumpdata dashboard.ColorParameter \
	--indent 2 > colorparameter.json

loaddata:
	uv run manage.py loaddata secretbox/tools/loaddata/colorparameter.json
	uv run manage.py loaddata secretbox/tools/loaddata/usergroup.json
	uv run manage.py loaddata secretbox/tools/loaddata/default_users.json
	uv run manage.py set_default_password

loaddata-test:
	uv run manage.py loaddata secretbox/tools/loaddata/colorparameter.json --settings=config.settings.test
	uv run manage.py loaddata secretbox/tools/loaddata/usergroup.json --settings=config.settings.test
	uv run manage.py loaddata secretbox/tools/loaddata/default_users.json --settings=config.settings.test
	uv run manage.py set_default_password --settings=config.settings.test