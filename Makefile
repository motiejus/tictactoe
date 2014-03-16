BIN ?= env/bin

.PHONY: all test cover style clean

all: env/.setup_done

test: cover style

env/.setup_done: env/bin/pip requirements.txt requirements_dev.txt
	$(BIN)/pip install --pre -rrequirements.txt -rrequirements_dev.txt
	touch $@

env/bin/pip:
	rm -fr env
	virtualenv -ppython3 env

cover: env/.setup_done
	$(BIN)/coverage run --source='tictactoe' -m tictactoe.manage test --noinput
	$(BIN)/coverage xml -o .coverage.xml
	$(BIN)/coverage html -d .htmlcov
	echo "  See .htmlcov/index.html for coverage report"

style: env/.setup_done
	$(BIN)/flake8 --exclude=migrations tictactoe setup.py

clean:
	rm -fr env
	find -name '*.py[co]' -exec rm {} \;
