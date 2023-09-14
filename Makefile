install:
	pipenv install

seed:
	python lib/seed.py

reset:
	python lib/reset.py

debug:
	python lib/debug.py

flask:
	python lib/app.py

env:
	export FLASK_APP=lib/app.py
	
upgrade:
	flask --app=lib/app.py db upgrade

downgrade:
	flask --app=lib/app.py db downgrade

migrate: 
	flask --app=lib/app.py db migrate -m "${m}"
