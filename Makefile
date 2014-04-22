BIN ?= env/bin

.PHONY: all test cover style clean setup go

all: setup

test: cover style

DJ=--find-links=https://www.djangoproject.com/m/releases/1.7/Django-1.7b1.tar.gz

setup: env/.env_done tictactoe/tictactoe.cfg

tictactoe/tictactoe.cfg:
	cp tictactoe/tictactoe.example.cfg $<

go: tictactoe/tictactoe.cfg env/.env_done
	$(BIN)/tictactoe runserver 0.0.0.0:8000

env/.env_done: env/bin/pip requirements.txt requirements_dev.txt
	$(BIN)/pip install -e . $(DJ) -rrequirements_dev.txt
	touch $@

env/bin/pip:
	rm -fr env
	virtualenv -ppython3 env

cover: env/.env_done
	$(BIN)/coverage run --source='tictactoe' -m tictactoe.manage test --noinput
	$(BIN)/coverage html -d .htmlcov
	echo "  See .htmlcov/index.html for coverage report"

style: env/.env_done
	$(BIN)/flake8 --exclude=migrations tictactoe setup.py

clean:
	rm -fr env
	find -name '*.py[co]' -exec rm {} \;
