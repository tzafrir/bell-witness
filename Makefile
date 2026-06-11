.PHONY: reproduce test expected

reproduce:
	python3 reproduce.py

test:
	python3 -m pytest -q tests/

expected:
	python3 reproduce.py --write-expected
