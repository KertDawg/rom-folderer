

all:

clean:
	rm -rf rom-folderer rom-folderer.exe *.spec build dmg

rom-folderer: Makefile src/main.py
	pyinstaller --onefile --distpath . -n rom-folderer src/main.py

rom-folderer.exe: Makefile src/main.py
	pyinstaller.exe --onefile --distpath . -n rom-folderer.exe src/main.py

dmg/rom-folderer.app: Makefile src/main.py
	mkdir -p dmg
	rm -rf dmg/*
	pyinstaller --onefile --osx-bundle-identifier=com.github.kertdawg.romfolderer --distpath dmg src/main.py
	osascript -e 'tell application "Finder"' -e '  set theTgt to POSIX file \"/Applications" as alias' -e '  make new alias to theTgt at POSIX file "dmg/Applications"' -e '  set name of result to "Applications"' -e 'end tell'"

rom-folderer.rw.dmg: Makefile dmg/rom-folderer.app
	hdiutil create rom-folderer.rw.dmg -ov -volname "Rom Folderer" -fs HFS+ -srcfolder dmg"

rom-folderer.dmg: Makefile rom-folderer.rw.dmg
	hdiutil convert rom-folderer.rw.dmg -format UDZO -o rom-folderer.dmg
