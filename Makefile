SHELL 				:=	/bin/bash
VENV_DIRECTORY_NAME	:=	venv
PYTHON_USER_BASE 	:=	$(shell python -m site --user-base)

create-virtualenv= \
	@echo "${GREEN}Create virtualenv in $(VENV_DIRECTORY_NAME) directory${RESET}"; \
	python $(PYTHON_USER_BASE)/bin/virtualenv -p python3.4 $(VENV_DIRECTORY_NAME)

install-requirements= \
	@./venv/bin/pip3 install -r $(CURDIR)/requirements/requirements-core.txt; \

install-virtualenv= \
	@echo "${GREEN}Install virtualenv locally for user${RESET}"; \
	pip install --user virtualenv -U

run-all-unit-test-with-green = \
	$(CURDIR)/$(VENV_DIRECTORY_NAME)/bin/green -c .green -s1 tests/unit; \

install:
	$(eval env ?= dev)
	$(call install-virtualenv)
	$(call create-virtualenv)
	$(call install-requirements,${env})

init:
	$(MAKE) install

remove-pyc:
	$(call remove-pyc)

tests: remove-pyc tests-unit

tests-unit:
	@echo -e "Run Unit tests."
	$(call run-all-unit-test-with-green)



.PHONY: init install tests tests-unit
