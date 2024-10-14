#!/usr/bin/python3

import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def PickDataFolder():
    #  Show the folder dialog.
    DataFolder.set(filedialog.askdirectory(title="Choose the data folder", initialdir=DataFolder.get()))
    LoadStructures()


def PickROMsFolder():
    #  Show the folder dialog.
    ROMsFolder.set(filedialog.askdirectory(title="Choose the ROMs folder", initialdir=ROMsFolder.get()))


def PickOutputFolder():
    #  Show the folder dialog.
    OutputFolder.set(filedialog.askdirectory(title="Choose the output folder", initialdir=OutputFolder.get()))


def LoadStructures():
    global StructureNamesList
    global StructuresList
    global SystemsList

    StructuresFileName = os.path.join(DataFolder.get(), "structures.csv")
    SystemsFileName = os.path.join(DataFolder.get(), "systems.csv")
    StructureNamesList = []
    StructuresList = []
    SystemsList = []

    #  Load the systems.
    with open(StructuresFileName, "r", encoding="utf-8-sig") as SystemsFile:
        SystemsReader = csv.DictReader(SystemsFile)

        for OneStructure in SystemsReader:
            if (OneStructure["Structure"] not in StructureNamesList):
                StructureNamesList.append(OneStructure["Structure"])
                StructuresList.append(OneStructure)

    StructureNamesList.sort()
    StructureChoice["values"] = StructureNamesList

    #  Load systems.
    with open(SystemsFileName, "r", encoding="utf-8-sig") as SystemsFile:
        SystemsReader = csv.DictReader(SystemsFile)

        for OneSystem in SystemsReader:
            SystemsList.append(OneSystem)


#  Copy files to the output folders.
def RunFoldering():
    #  Calculate progress bar values.
    NumberOfSystems = len(SystemsList)
    ProgressStep = 100 / NumberOfSystems
    CurrentSystem = 1

    #  Loop through systems.
    for OneSystem in SystemsList:
        RunProgressValue.set(ProgressStep * CurrentSystem)
        ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="{:g}%".format(RunProgressValue.get()), anchor="center")
        CurrentSystem = CurrentSystem + 1

        #  Find the folder(s) for that system.
        SystemFolders = FindFoldersForSystem(OneSystem["System"])


def FindFoldersForSystem(SystemName):
    FolderNames = []

    #  Get keywords for this system.
    Keywords = GetKeywordsForSystem(SystemName)

    #  Loop through the source folders.
    for FolderName in os.listdir(ROMsFolder.get()):
        if os.path.isdir(os.path.join(ROMsFolder.get(), FolderName)):
            #  Loop through the keywords.
            for Keyword in Keywords:
                if (FolderName.lower() == Keyword.lower()):
                    FolderNames.append(FolderName)
                
    return FolderNames


def GetKeywordsForSystem(SystemName):
    #  Loop through the systems.
    Keywords = []

    for OneSystem in SystemsList:
        #  Find the keywords for that system.
        if (OneSystem["System"] == SystemName):
            Keywords.append(OneSystem["Keyword"])

    return Keywords


MainWindow = tk.Tk()
MainWindow.title("Rom Folderer")
MainMenu = tk.Menu(MainWindow)

DataFolder=tk.StringVar()
DataFolder.set(os.path.join(os.getcwd(), "data"))
ROMsFolder=tk.StringVar()
ROMsFolder.set(os.getcwd())
OutputFolder=tk.StringVar()
OutputFolder.set(os.getcwd())
RunProgressValue = tk.DoubleVar()
RunProgressValue.set(0)
StructureNamesList = []
StructuresList = []
SystemsList = []

FileMenu = tk.Menu(MainMenu, tearoff=0)
FileMenu.add_command(label="Exit", command=MainWindow.destroy)
MainMenu.add_cascade(label="File", menu=FileMenu)

DataFolderLabel = tk.Label(MainWindow, text="Data Folder")
DataFolderEntry = tk.Entry(MainWindow, textvariable=DataFolder, width=40)
DataFolderButton = tk.Button(MainWindow, text="...", command=PickDataFolder)
DataFolderLabel.grid(row=0, column=0, sticky="e")
DataFolderEntry.grid(row=0, column=1, sticky="ew")
DataFolderButton.grid(row=0, column=2, sticky="ew")

StructuresLabel = tk.Label(MainWindow, text="Output Structure")
StructureChoice = ttk.Combobox(MainWindow, values=StructureNamesList)
StructuresLabel.grid(row=1, column=0, sticky="e")
StructureChoice.grid(row=1, column=1, sticky="ew")

ROMsFolderLabel = tk.Label(MainWindow, text="ROMs Folder")
ROMsFolderEntry = tk.Entry(MainWindow, textvariable=ROMsFolder, width=40)
ROMsFolderButton = tk.Button(MainWindow, text="...", command=PickROMsFolder)
ROMsFolderLabel.grid(row=2, column=0, sticky="e")
ROMsFolderEntry.grid(row=2, column=1, sticky="ew")
ROMsFolderButton.grid(row=2, column=2, sticky="ew")

OutputFolderLabel = tk.Label(MainWindow, text="Output Folder")
OutputFolderEntry = tk.Entry(MainWindow, textvariable=OutputFolder, width=40)
OutputFolderButton = tk.Button(MainWindow, text="...", command=PickOutputFolder)
OutputFolderLabel.grid(row=3, column=0, sticky="e")
OutputFolderEntry.grid(row=3, column=1, sticky="ew")
OutputFolderButton.grid(row=3, column=2, sticky="ew")

ProgressBarStyle = ttk.Style(MainWindow)
ProgressBarStyle.layout("text.Horizontal.TProgressbar", 
             [("Horizontal.Progressbar.trough",
               {"children": [("Horizontal.Progressbar.pbar",
                              {"side": "left", "sticky": "ns"})],
                "sticky": "nswe"}), 
              ("Horizontal.Progressbar.label", {"sticky": "nswe"})])
ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="0%", anchor="center")

RunButton = tk.Button(MainWindow, text="Run...", command=RunFoldering)
RunButton.grid(row=4, column=0)
RunProgress = ttk.Progressbar(MainWindow, maximum=100, style="text.Horizontal.TProgressbar", variable=RunProgressValue)
RunProgress.grid(row=4, column=1, columnspan=2, sticky="ew")

LoadStructures()
MainWindow.config(menu=MainMenu)
MainWindow.mainloop()
