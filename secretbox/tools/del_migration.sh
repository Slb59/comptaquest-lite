# !!! cette commande casse l'environnement de développement .venv!!!
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete