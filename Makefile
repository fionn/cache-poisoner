SRC = main.py

export PIP_DISABLE_PIP_VERSION_CHECK=1

venv: requirements.txt requirements_dev.txt
	@python3 -m venv $@
	@source $@/bin/activate && pip install -r $< -r requirements_dev.txt
	@echo "enter virtual environment: source $@/bin/activate"

.PHONY: outdated
outdated: venv
	@source $</bin/activate && pip list --$@

tags: $(SRC)
	@ctags --languages=python --python-kinds=-i $(SRC)

.PHONY: lint
lint:
	@pylint -f colorized $(SRC)

.PHONY: typecheck
typecheck:
	@mypy $(SRC)

.PHONY: clean
clean:
	@$(RM) -r .mypy_cache/
	@$(RM) -r __pycache__/
	@$(RM) tags
