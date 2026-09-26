install:
	@uv sync
run:
	@uv run python3 pac-man.py config.json
debug:
	@uv run python3 -m pdb
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache .pytest_cache
lint:
	@flake8 .
	@mypy .	--warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \