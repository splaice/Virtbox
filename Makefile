.PHONY: all pep8 pyflakes clean dev shell nuke nuke-vm nuke-hdd

GITIGNORES=$(shell cat .gitignore |tr "\\n" ",")

all: pep8 pyflakes

pep8: .gitignore env
	bin/virtual-env-exec pep8 . --exclude=$(GITIGNORES)

pyflakes: env
	bin/virtual-env-exec pyflakes virtbox tests

dev: env env/.pip

env:
	virtualenv --distribute env

env/.pip: env cfg/requirements.txt
	bin/virtual-env-exec pip install -r cfg/requirements.txt
	bin/virtual-env-exec pip install -e .
	touch env/.pip

test: pep8 pyflakes env/.pip nuke
	sudo su virtbox -c "bin/virtual-env-exec testify tests"

shell:
	bin/virtual-env-exec ipython

devclean:
	@rm -rf env

clean:
	@rm -rf build dist env

nuke-vm:
	@sudo su virtbox -c "bin/nuke-all-vm.sh"

nuke-hdd:
	@sudo su virtbox -c "bin/nuke-all-hdd.sh"

nuke: nuke-vm nuke-hdd
