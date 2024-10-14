#!/usr/bin/python3

import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def PickFolder():
    #  Show the filder dialog.
    DataFolder.set(filedialog.askdirectory(title="Choose the data folder", initialdir=DataFolder.get()))
    LoadStructures()


def LoadStructures():
    StructuresFileName = os.path.join(DataFolder.get(), "structures.csv")

    #  Load the systems.
    StructuresList = []

    with open(StructuresFileName, "r", encoding="utf-8-sig") as SystemFile:
        SystemReader = csv.DictReader(SystemFile)

        for OneSystem in SystemReader:
            if (OneSystem["Structure"] not in StructuresList):
                StructuresList.append(OneSystem["Structure"])

    StructuresList.sort()
    StructureChoice["values"] = StructuresList


MainWindow = tk.Tk()
MainWindow.title("Rom Folderer")
MainMenu = tk.Menu(MainWindow)

DataFolder=tk.StringVar()
DataFolder.set(os.path.join(os.getcwd(), "data"))
StructuresList = []

FileMenu = tk.Menu(MainMenu, tearoff=0)
FileMenu.add_command(label="Exit", command=MainWindow.destroy)
MainMenu.add_cascade(label="File", menu=FileMenu)

FolderLabel = tk.Label(MainWindow, text="Data Folder")
FolderEntry = tk.Entry(MainWindow, textvariable=DataFolder, width=40)
FolderButton = tk.Button(MainWindow, text="...", command=PickFolder)
FolderLabel.grid(row=0, column=0, sticky="e")
FolderEntry.grid(row=0, column=1, sticky="ew")
FolderButton.grid(row=0, column=2, sticky="ew")

StructuresLabel = tk.Label(MainWindow, text="Structure")
StructureChoice = ttk.Combobox(MainWindow, values=StructuresList)
StructuresLabel.grid(row=1, column=0, sticky="e")
StructureChoice.grid(row=1, column=1, sticky="ew")

LoadStructures()
MainWindow.config(menu=MainMenu)
MainWindow.mainloop()
