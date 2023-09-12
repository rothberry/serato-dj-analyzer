install:
	pipenv install

seed:
	python lib/seed.py

debug:
	python lib/debug.py

flask:
	python lib/app.py

env:
	export FLASK_APP=lib/app.py