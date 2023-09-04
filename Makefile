install:
	pipenv install

seed:
	python lib/seed.py

debug:
	python lib/debug.py

flask:
	python lib/app.py