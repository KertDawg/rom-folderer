
bin_PROGRAMS = rom-folderer$(EXEEXT)
rom_folderer_SOURCES = src/main.py

rom-folderer$(EXEEXT): Makefile src/main.py
	pyinstaller --onefile --distpath . -n rom-folderer src/main.py
