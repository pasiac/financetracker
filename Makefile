run:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
test:
	python manage.py test
linters:
	sh -c "isort --skip-glob=.tox --recursive . "
	sh -c "black ."
venv:
	sh -c "source $HOME/foodenv/bin/activate"