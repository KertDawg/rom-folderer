#!/usr/bin/python3

import os
import shutil
import glob
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


DEBUGMODE = False



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

    StructuresFileName = os.path.join(DataFolder.get(), "structures.csv")
    StructureNamesList = []
    StructuresList = []

    with open(StructuresFileName, "r", encoding="utf-8-sig") as StructuresFile:
        StructuresReader = csv.DictReader(StructuresFile)

        for OneStructure in StructuresReader:
            if (OneStructure["Structure"] not in StructureNamesList):
                StructureNamesList.append(OneStructure["Structure"])

            StructuresList.append(OneStructure)

    StructureNamesList.sort()
    StructureChoice["values"] = StructureNamesList

    #  Enable the load everything else button.
    StructureChoice["state"] = "active"
    StructuresLabel["fg"] = "green"
    LoadDataButton["bg"] = "lightgray"

    #  Disable the run button.
    RunButton["state"] = "disabled"


def LoadEverythingElse(EventObject):
    global SystemsList

    SystemsFileName = os.path.join(DataFolder.get(), "systems.csv")
    SystemsList = []

    #  Load the systems.
    with open(SystemsFileName, "r", encoding="utf-8-sig") as SystemsFile:
        SystemsReader = csv.DictReader(SystemsFile)

        for OneSystem in SystemsReader:
            SystemsList.append(OneSystem)

    #  Enable the run button.
    RunButton["state"] = "active"
    RunButton["bg"] = "green"
    StructuresLabel["fg"] = "black"


#  Copy files to the output folders.
def RunFoldering():
    ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="Figuring out folders...", anchor="center")
    RunButton["state"] = "disabled"
    RunButton["bg"] = "grey"
    MainMenu.update()
    

    #  Get the information for the target structure and mapping.
    StructureFolders = []
    Mapping = []

    for OneStructure in StructuresList:
        if (OneStructure["Structure"].lower() == SelectedStructureName.get().lower()):
            StructureFolders.append(OneStructure)

    #  Loop through systems.
    SystemNames = []
    for OneSystem in SystemsList:
        if (not OneSystem["System"].lower() in SystemNames):
            SystemNames.append(OneSystem["System"].lower())

            #  Get the keywords for the system.
            if DEBUGMODE:
                print("SystemName: ", OneSystem["System"])

            Keywords = GetKeywordsForSystem(OneSystem["System"])

            #  Get the folder(s) for that system.
            SourceFolders = FindFoldersForSystem(Keywords)

            #  Get the destination folder.  Set it to something silly in case this fails.
            DestinationFolder = "///NULL"

            for OneStructure in StructureFolders:
#                Keywords.append(OneStructure["Folder"].lower())

                if DEBUGMODE:
                    print("  Testing folder: ", OneStructure)

                if (OneStructure["Folder"].lower() in Keywords):
                    DestinationFolder = os.path.join(OutputFolder.get(), OneStructure["Folder"])

                    if DEBUGMODE:
                        print("  DestinationFolder", DestinationFolder)

            #  Now that we have the folders.  Add them to the mapping.
            for OneSourceFolder in SourceFolders:
                if (not DestinationFolder == "///NULL"):
                    if DEBUGMODE:
                        print("  Copying folder ", OneSourceFolder, " to ", DestinationFolder)

                    Mapping.append({ "From": OneSourceFolder, "To": DestinationFolder })

    #  Get full file paths.
    ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="Figuring out files...", anchor="center")
    MainMenu.update()
    FilesToCopy = []

    for Map in Mapping:
        for OneFile in glob.glob(os.path.join(ROMsFolder.get(), Map["From"], "*"), recursive=True):
            if not os.path.isdir(OneFile):
                FilesToCopy.append({ "From": OneFile, "To": os.path.join(OutputFolder.get(), Map["To"])})

    #  Calculate progress bar values.
    FilesToCopyLength = len(FilesToCopy)
    ProgressStep = 100 / (FilesToCopyLength if (FilesToCopyLength > 0) else 1)
    CurrentMap = 1

    for OneFile in FilesToCopy:
        RunProgressValue.set(ProgressStep * CurrentMap)
        ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="{:10.1f}%".format(RunProgressValue.get()), anchor="center")
        MainMenu.update()
        CurrentMap = CurrentMap + 1

        #  Make the folder if necessary.
        if not os.path.exists(OneFile["To"]):
            if DEBUGMODE:
                print("  Creating folder: ", OneFile["To"])
            
            if (not DEBUGMODE):
                os.makedirs(OneFile["To"])

        #  Copy files.
        if not (DEBUGMODE):
            shutil.copy(OneFile["From"], OneFile["To"])


def FindFoldersForSystem(Keywords):
    FolderNames = []

    #  Loop through the source folders.
    for FolderName in os.listdir(ROMsFolder.get()):
        if os.path.isdir(os.path.join(ROMsFolder.get(), FolderName)):
            #  Loop through the keywords.
            for Keyword in Keywords:
                if ((FolderName.lower() == Keyword.lower()) and not (FolderName.lower() in FolderNames)):

                    FolderNames.append(FolderName)

    if DEBUGMODE:
        print("  Folders: ", FolderNames)

    return FolderNames


def GetKeywordsForSystem(SystemName):
    #  Loop through the systems.
    Keywords = [SystemName.lower()]

    for OneSystem in SystemsList:
        #  Find the keywords for that system.
        if (OneSystem["System"].lower() == SystemName.lower()):
            #  Split the keywords into an array.
            KeywordArray = OneSystem["Keyword"].lower().strip().replace('"', '').strip().split(",")

            for Keyword in KeywordArray:
                Keywords.append(Keyword)

    if DEBUGMODE:
        print("  Keywords: ", Keywords)

    return Keywords


MainWindow = tk.Tk()
MainWindow.title("ROM Folderer")
MainMenu = tk.Menu(MainWindow)

DataFolder=tk.StringVar()
DataFolder.set(os.path.join(os.getcwd(), "data"))
ROMsFolder=tk.StringVar()
ROMsFolder.set("/mnt/d/Emulators/LaunchBox/Games")#os.path.join(os.getcwd(), "input"))
OutputFolder=tk.StringVar()
OutputFolder.set("/mnt/d/Emulators/rom-folderer-test")#os.path.join(os.getcwd(), "output"))
RunProgressValue = tk.DoubleVar()
RunProgressValue.set(0)
StructureNamesList = []
StructuresList = []
SystemsList = []
SelectedStructureName = tk.StringVar()
SelectedStructureName.set("")

FileMenu = tk.Menu(MainMenu, tearoff=0)
FileMenu.add_command(label="Exit", command=MainWindow.destroy)
MainMenu.add_cascade(label="File", menu=FileMenu)

DataFolderLabel = tk.Label(MainWindow, text="Data Folder")
DataFolderEntry = tk.Entry(MainWindow, textvariable=DataFolder, width=40)
DataFolderButton = tk.Button(MainWindow, text="...", command=PickDataFolder)
DataFolderLabel.grid(row=0, column=0, sticky="e", padx=8, pady=8)
DataFolderEntry.grid(row=0, column=1, sticky="ew", padx=8, pady=8)
DataFolderButton.grid(row=0, column=2, sticky="ew", padx=8, pady=8)

LoadDataButton = tk.Button(MainWindow, text="Load Data", command=LoadStructures, bg="green")
LoadDataButton.grid(row=1, column=2, sticky="ew", padx=8, pady=8)

StructuresLabel = tk.Label(MainWindow, text="Output Structure")
StructureChoice = ttk.Combobox(MainWindow, values=StructureNamesList, textvariable=SelectedStructureName, state="disabled")
StructureChoice.bind("<<ComboboxSelected>>", LoadEverythingElse)
StructuresLabel.grid(row=2, column=0, sticky="e", padx=8, pady=8)
StructureChoice.grid(row=2, column=1, sticky="ew", padx=8, pady=8)

ROMsFolderLabel = tk.Label(MainWindow, text="ROMs Folder")
ROMsFolderEntry = tk.Entry(MainWindow, textvariable=ROMsFolder, width=40)
ROMsFolderButton = tk.Button(MainWindow, text="...", command=PickROMsFolder)
ROMsFolderLabel.grid(row=4, column=0, sticky="e", padx=8, pady=8)
ROMsFolderEntry.grid(row=4, column=1, sticky="ew", padx=8, pady=8)
ROMsFolderButton.grid(row=4, column=2, sticky="ew", padx=8, pady=8)

OutputFolderLabel = tk.Label(MainWindow, text="Output Folder")
OutputFolderEntry = tk.Entry(MainWindow, textvariable=OutputFolder, width=40)
OutputFolderButton = tk.Button(MainWindow, text="...", command=PickOutputFolder)
OutputFolderLabel.grid(row=5, column=0, sticky="e", padx=8, pady=8)
OutputFolderEntry.grid(row=5, column=1, sticky="ew", padx=8, pady=8)
OutputFolderButton.grid(row=5, column=2, sticky="ew", padx=8, pady=8)

ProgressBarStyle = ttk.Style(MainWindow)
ProgressBarStyle.layout("text.Horizontal.TProgressbar", 
             [("Horizontal.Progressbar.trough",
               {"children": [("Horizontal.Progressbar.pbar",
                              {"side": "left", "sticky": "ns"})],
                "sticky": "nswe"}), 
              ("Horizontal.Progressbar.label", {"sticky": "nswe"})])
ProgressBarStyle.configure("text.Horizontal.TProgressbar", text="0%", anchor="center")

RunButton = tk.Button(MainWindow, text="Run...", command=RunFoldering, state="disabled")
RunButton.grid(row=6, column=0, padx=8, pady=8)
RunProgress = ttk.Progressbar(MainWindow, maximum=100, style="text.Horizontal.TProgressbar", variable=RunProgressValue)
RunProgress.grid(row=6, column=1, columnspan=2, sticky="ew", padx=8, pady=8)

MainWindow.config(menu=MainMenu)
MainWindow.mainloop()
