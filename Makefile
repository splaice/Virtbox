.PHONY: all pep8 pyflakes clean dev

GITIGNORES=$(shell cat .gitignore |tr "\\n" ",")

all: pep8 pyflakes

pep8: .gitignore env
	bin/virtual-env-exec pep8 . --exclude=$(GITIGNORES)

pyflakes: env
	bin/virtual-env-exec pyflakes virtbox tests

dev: env env/.pip

env:
	virtualenv --distribute env

env/.pip: env requirements.txt
	bin/virtual-env-exec pip install -r requirements.txt
	bin/virtual-env-exec pip install -e .
	touch env/.pip

test: pep8 pyflakes env/.pip
	sudo su virtbox -c "bin/virtual-env-exec testify tests"

devclean:
	@rm -rf env

clean:
	@rm -rf build dist env
