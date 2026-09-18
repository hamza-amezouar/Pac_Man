install:
	uv sync
run:
	uv run python3 -m game
debug:
	uv run python3 -m pdb
clean:
	find . -type -d name -exec "__pycache__" rm -rf {} +