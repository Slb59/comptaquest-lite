quality:
	uv run black .
	uv run isort .
	uv run flake8 .

deploy:
	uv pip freeze > requirements.txt
	rsync -a --exclude-from='.deployignore' . "/home/sylvie/Documents/01_Documents Slb/01-Journaling/SecretBox/"
	cp secretbox.desktop ~/Bureau/
	cd "/home/sylvie/Documents/01_Documents Slb/01-Journaling/SecretBox/"
	uv add -r requirements.txt

