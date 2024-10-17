

all:

clean:
	rm -rf rom-folderer *.spec build

rom-folderer: Makefile src/Main.py
	pyinstaller --onefile --distpath . -n rom-folderer src/main.py



