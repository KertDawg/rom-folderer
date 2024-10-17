

all:

clean:
	rm -rf rom-folderer rom-folderer.exe *.spec build

rom-folderer: Makefile src/Main.py
	pyinstaller --onefile --distpath . -n rom-folderer src/main.py

rom-folderer.exe: Makefile src/Main.py
	pyinstaller.exe --onefile --distpath . -n rom-folderer.exe src/main.py


