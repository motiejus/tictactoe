BIN ?= env/bin

.PHONY: all test cover style

all: env/.state

test: cover style

env/.state: requirements.txt requirements_dev.txt
	rm -fr env
	virtualenv -ppython3 env
	$(BIN)/pip install --pre -rrequirements.txt -rrequirements_dev.txt
	touch $@

cover: env/.state
	$(BIN)/coverage run --source='tictactoe' -m tictactoe.manage test --noinput
	$(BIN)/coverage xml -o .coverage.xml
	$(BIN)/coverage html -d .htmlcov
	echo "  See .htmlcov/index.html for coverage report"

style: env/.state
	$(BIN)/flake8 --exclude=migrations tictactoe setup.py
