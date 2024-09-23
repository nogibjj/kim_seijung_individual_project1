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
	git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
	git config --local user.name "github-actions[bot]"
	git add Amazon_Sales_Report.pdf
	git commit -m "Add updated report"
	git push
		
all: install lint test format