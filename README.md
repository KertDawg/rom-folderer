# rom-folderer
ROM Folderer finds video game ROMs in a given folder structure and places them in a new folder in a structure useful for a specific emulator.

## The Problem
Different emulators and launchers want ROMs in a folder structure that is specific to that emulator.  If you have more than one system, this can get ugly.  Synchronizing these emulators takes time and is error prone.  You can miss a ROM or folder.

## ROM Folderer
This program can be configured with CSV files to find ROMs in a source folder.  Then, a structure is chosen for the target emulator.  The program will then copy the files from the source folders to the right output folder.

##  Running It
If you have Python 3 installed, you can just run `src/main.py`.  You can also build (or download) and run a compiled executable for your platform.

## Building Binaries

Requirements:
- Python 3 in the path
- PyInstaller in the path

### Windows
- Run `make rom-folderer.exe`

### WSL 2
- Run `make rom-folderer`

### macOS Homebrew
- Run `make rom-folderer`

## To Do
1. Implement error handling
1. Add more structures for target emulators
1. Implement native build for macOS

