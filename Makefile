install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python3 -m pytest -vv --cov=main test_*.py
	py.test --nbval *.ipynb

format:
	nbqa black *.ipynb &&\
	black *.py && black test_*.py

lint:
	ruff check test_*.py && ruff check *.py
	nbqa ruff *.ipynb

deploy:
	echo "No deployment steps specified yet."
		
all: install lint test format