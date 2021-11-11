test:
	./tools/runtests.sh

run:
	python3 abcted/main.py

install-mint-deps:
	apt install python3 python3-venv python3-tk fluidsynth fluid-soundfont-gm fluid-soundfont-gs
