test:
	./tools/runtests.sh

run:
	python3 abcted/main.py

doc:
	cd docs && make html

install-mint-deps:
	apt install python3 python3-venv python3-tk fluidsynth fluid-soundfont-gm fluid-soundfont-gs

help:
	@echo "Makefile targets:"
	@echo "    test: run unit tests"
	@echo "    run: run abcted"
	@echo "    doc: build documentation in HTML format"
	@echo "    install-mint-deps: install packages needed by abcted on a Linux Mint distribution"
	@echo "    help: show the Makefile targets"
