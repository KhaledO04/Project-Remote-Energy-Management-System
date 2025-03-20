# Testing values

functionTest1 = "Natfunktion"

functionTest2 = "Morgenfunktion"

roomTest1 = "Stue"

roomTest2 = "Køkken"

roomTest3 = "Badeværelse"

editTest = [5, 10, 7, 12]
editTest2 = [2.0, 14.5, 8.3, 10.8]


def InitFiles():
    try:
        with open("rooms.txt", "x+", encoding="UTF-8") as rooms:
            rooms.write("Room ID counter: 0")
            print("FILE CREATION COMPLETE")

    except FileExistsError:
        print("rooms.txt already exists!")
    
    try:
        with open("functions.txt", "x+", encoding="UTF-8") as functions:
            functions.write("Function ID counter: 0\n")

    except FileExistsError:
        print("functions.txt already exists!")
    

# Creates the settings file with all the values
def InitSettings(elecSupplier, postalCode):
    try:
        with open("settings.txt", "x+", encoding="UTF-8") as settings:
            settings.writelines([f"{elecSupplier}", f"\n {str(postalCode)}"])
    except FileExistsError:
        print("settings.txt already exists!")


# Initial valuese for rooms/functions
def InitWrite(file, ID, name):
    ID += 1

    file.write(f'\n{name}:\n')
    file.write(f"ID: {ID}\n")
    file.write(f"Prisloft: 0.0\n")
    file.write(f"Temperatur: 0.0\n")
    file.write(f"Markør (høj): 0.0\n")
    file.write(f"Markør (lav): 0.0\n")

    return ID

# Retrieves the ID from the ID counter in a file
def GetIdCount(filename):
    with open(filename, "r") as file:
        file.seek(0)
        idLine = file.readline()
        splitId = idLine.split()
        id = int(splitId[-1].strip("\n"))
        return id

#Adds a function/room to file
def AddToFile(filename, name):

    id = GetIdCount(filename)


    with open(filename, "a", encoding="UTF-8") as file:
            id = InitWrite(file, id, name)

    with open(filename, "r") as file:
        lines = file.readlines()
        splitId = lines[0].split()
        
        # Change id to the incremented one
        splitId[-1] = str(id)
        lines[0] = " ".join(splitId) + "\n"

    with open(filename, "w") as file:
        file.writelines(lines)


# Gets a function or room from file
def GetDataFromFile(filename, ID):
    with open(filename, "r", encoding="UTF-8") as file:
        firstline = file.readline()
        file.seek(len(firstline)) # Skips the first line (ID counter)
        lines = file.readlines()
        attributes = {
            "name": "",
            "id": 0,
            "prisloft": 0.0,
            "temperatur": 0.0,
            "markerHigh": 0.0,
            "markerLow": 0.0,
        }

        for i, line in enumerate(lines):
            if line.strip("\n") and str(ID) == line.split()[-1]:
                found = lines[i-1:i+5]

                for j, foundLine in enumerate(found):
                    if foundLine.split()[-1].strip("\n").isdigit():
                        attributes["id"] = int(foundLine.split()[-1].strip("\n"))
                    
                    else:
                        try:
                            if foundLine.split(":")[0] == "Prisloft":
                                attributes["prisloft"] = float(foundLine.split()[-1].strip("\n"))
                            elif foundLine.split(":")[0] == "Temperatur":
                                attributes["temperatur"] = float(foundLine.split()[-1].strip("\n"))
                            elif foundLine.split(":")[0] == "Markør (høj)":
                                attributes["markerHigh"] = float(foundLine.split()[-1].strip("\n"))
                            elif foundLine.split(":")[0] == "Markør (lav)":
                                attributes["markerLow"] = float(foundLine.split()[-1].strip("\n"))
                            else:
                                attributes["name"] = float(foundLine.split()[-1].strip("\n"))
                        except ValueError:
                            attributes["name"] = foundLine.strip(":\n")
                return attributes
               
    

def GetAll(filename):

    id = GetIdCount(filename)

    # List for appending elements
    list = []

    for i in range(id):
        data = GetDataFromFile(filename, i+1)
        if data is not None:
            list.append(data)
    
    return list


# Edits all lines in file
# "search" should me equal to function/room name
# "editList" is the edited list to insert
def EditLines(filename, ID, editList):
    with open(filename, "r", encoding="UTF-8") as file:
        firstline = file.readline()
        file.seek(len(firstline)) # Skips the first line (ID counter)
        lines = file.readlines()

    for index, line in enumerate(lines):
        if line.strip("\n") and str(ID) == line.split()[-1].strip("\n"):
            # Slices the lines list to contain a functions/rooms elements
            for i, data in enumerate(lines[index+1:index+5]):
                splitData = data.split()
                splitData[-1] = str(editList[i])
                lines[index+1+i] = " ".join(splitData) + "\n"
            # Needs break so it doesnt loop through the whole text document
            break
    
    lines[0] = firstline

    with open(filename, "w", encoding="UTF-8") as file:
        file.writelines(lines)

# Edits a specific line in a function or room
def EditLine(filename, searchArea, searchLine, newValue):
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()

        for index, area in enumerate(lines):
            if searchArea == area.strip(":\n"):
                foundArea =  lines[index+2:index+6]
                break

        for i, line in enumerate(foundArea):
            if searchLine == line.split(":")[0]:
                splitLine = foundArea[i].split()
                splitLine[-1] = str(newValue)
                foundArea[i] = " ".join(splitLine) + "\n"
                lines[index+2:index+6] = foundArea
                break
                
    with open(filename, "w", encoding="UTF-8") as file:
        file.writelines(lines)


# Deletes function or room
def DeleteInFile(filename, ID):
    with open(filename, "r", encoding="UTF-8") as file:
        firstline = file.readline() 
        file.seek(len(firstline)) 
        lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip("\n") and str(ID) == line.strip(":\n").split()[-1]:
                del lines[i-1:i+6]
                break
        
        lines[0] = firstline
    
    with open(filename, "w", encoding="UTF-8") as file:
        file.writelines(lines)


InitFiles()
InitSettings("NRGI", 8500)