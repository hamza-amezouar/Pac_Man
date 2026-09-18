install:
	@uv sync
run:
	@uv run python3 -m src
debug:
	@uv run python3 -m pdb
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +