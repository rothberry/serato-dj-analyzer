install:
	pipenv install

seed:
	python -m lib.seed
	# python lib/seed.py

reset:
	python lib/reset.py

debug:
	python debug.py

flask:
	python app.py

env:
	export FLASK_APP=app.py
	
upgrade:
	flask db upgrade
	# flask --app=lib/app.py db upgrade

downgrade:
	flask db downgrade
	# flask --app=lib/app.py db downgrade

migrate: 
	flask db migrate -m "${m}"
	# flask --app=lib/app.py db migrate -m "${m}"

run:
	python run.py

ui:
	pyuic6 gui/upload-gui.ui -o gui/template.py 