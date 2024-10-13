
bin_PROGRAMS = rom-folderer
rom_folderer_SOURCES = src/main.py

rom-folderer: Makefile src/main.py
	pyinstaller --onefile --distpath . -n rom-folderer src/main.py
