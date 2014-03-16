BIN ?= env/bin

.PHONY: all test cover style clean

all: env/.setup_done

test: cover style

env/.setup_done: requirements.txt requirements_dev.txt
	if [ -f $@ ]; then \
		$(BIN)/pip install --pre -rrequirements.txt -rrequirements_dev.txt; \
		touch $@; \
	else \
		rm -fr env; \
		virtualenv -ppython3 env; \
		$(BIN)/pip install --pre -rrequirements.txt -rrequirements_dev.txt; \
		touch $@; \
	fi

cover: env/.setup_done
	$(BIN)/coverage run --source='tictactoe' -m tictactoe.manage test --noinput
	$(BIN)/coverage xml -o .coverage.xml
	$(BIN)/coverage html -d .htmlcov
	echo "  See .htmlcov/index.html for coverage report"

style: env/.setup_done
	$(BIN)/flake8 --exclude=migrations tictactoe setup.py

clean:
	rm -fr env
