from math import sin
import subprocess
import string
from more_itertools import locate
import random
import os
import shutil
from difflib import SequenceMatcher

# helper functions
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def findIndices(lst: list, val):
    """ Function to find all indices of a given value in a list\n
    Args:
        lst: List to search for values
        val: Value to find indices
    Returns:
        List of indices of a given value in a list
    """

    indices = locate(lst, lambda x: x == val)
    return list(indices)

def similarity(str1: string, str2: string):
    """ Function to calculate similarity of two given strings\n
    Args:
        str1, str2: Strings to calculate similarity
    Returns:
        Similarity ratio of two given strings
    """
    return SequenceMatcher(None, str1, str2).ratio()

def clearFileFolder():
    """ Function to clear test file folder """

    folder = os.getcwd() + "\\testFiles"
    try:
        for filename in os.listdir(folder):
            filePath = os.path.join(folder, filename)

            if os.path.isfile(filePath) or os.path.islink(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
    except FileNotFoundError:
        os.mkdir(folder)

def getCharacters(lowercase = True, uppercase = True, digits = True, punctuation = True, spaces = True, newLines = True) -> list[str]:
    """ Function that returns a list of characters\n
    Args:
        lowercase: Include lowercase letters in the return list. Defaults to True
        uppercase: Include uppercase letters in the return list. Defaults to True
        digits: Include digits in the return list. Defaults to True
        punctuation: Include punctuation in the return list. Defaults to True
        spaces: Include spaces in the return list. Defaults to True
        newLines: Include new line symbol in the return list. Defaults to True
    Returns:
        List of selected characters
    """
    
    characters = []

    if lowercase:
        characters += list(string.ascii_lowercase)
    if uppercase:
        characters += list(string.ascii_uppercase)
    if digits:
        characters += list(string.digits)
    if punctuation:
        characters += list(string.punctuation)
    if spaces:
        characters += [" "]
    if newLines:
        characters += ["\n"]

    return characters

def getRandomString(length: int) -> str:
    """ Function that generates random string\n
    Args:
        length: Length of generated string
    Returns:
        Generated string
    """

    characters = getCharacters()
    str = ''.join(random.choice(characters) for _ in range(length))

    return str

def singleSymbol(numberOfFiles: int) -> list[str]:
    """ Function to generate text files with one random symbol\n
    Args:
        numberOfFiles: Number of files to generate
    Returns:
        List of the names of generated files
    """
    clearFileFolder()

    characters = getCharacters()
    numberOfFiles = len(characters) if numberOfFiles > len(characters) else numberOfFiles

    files = []
    for i in range(numberOfFiles):
        char = random.choice(characters)
        characters.remove(char)

        fileName = f"./testFiles/{i}.txt"

        f = open(fileName, "w")
        f.write(char)
        f.close()

        files.append(fileName)

    return files

def randomSymbols(numberOfFiles: int, numberOfSymbols: int) -> list[str]:
    """ Function to generate text files with random symbols\n
    Args:
        numberOfFiles: Number of files to generate
        numberOfSymbols: Number of symbols to generate in every file
    Returns:
        List of the names of generated files
    """
    clearFileFolder()
    
    files = []
    for i in range(numberOfFiles):
        str = getRandomString(numberOfSymbols)

        fileName = f"./testFiles/{i}.txt"

        f = open(fileName, "w")
        f.write(str)
        f.close()

        files.append(fileName)

    return files

def similarSymbols(numberOfFiles: int, numberOfSymbols: int) -> list[str]:
    """ Function to generate text files with strings that differ from first file by only one symbol\n
    Args:
        numberOfFiles: Number of files to generate
        numberOfSymbols: Number of symbols to generate in every file
    Returns:
        List of the names of generated files
    """

    clearFileFolder()
    
    characters = getCharacters()
    baseString = getRandomString(numberOfSymbols)

    if numberOfFiles < 1:
        return []

    files = ["./testFiles/0.txt"]

    f = open(f"./testFiles/0.txt", "w")
    f.write(baseString)
    f.close()

    generated = []

    for i in range(1, numberOfFiles):
        str = baseString

        while str == baseString or (str in generated):
            char = random.choice(characters)
            index = random.randint(0, numberOfSymbols - 1)
            str = str[0:index] + char + str[index + 1: ]

        generated.append(str)

        fileName = f"./testFiles/{i}.txt"

        f = open(fileName, "w")
        f.write(str)
        f.close()

        files.append(fileName)

    return files

def emptyFile(numberOfFiles: int) -> list[str]:
    """ Function to generate empty text files\n
    Args:
        numberOfFiles: Number of files to generate
    Returns:
        List of the names of generated files
    """

    clearFileFolder()

    files = []

    for i in range(numberOfFiles):
        fileName = f"./testFiles/{i}.txt"

        f = open(fileName, "w")
        f.close() 
    
        files.append(fileName)

    return files

def constitutionLines() -> list[str]:
    """ Function to get Lithuanian constitution text\n
    Returns:
        List of file names with constitution lines
    """

    f = open("konstitucija.txt", "r", encoding="utf8")
    lines = f.readlines()

    files = []

    for i in range(len(lines)):
        fileName = f"./testFiles/{i}.txt"
        
        f = open(fileName, "w", encoding="utf8")
        f.write(lines[i][0:-1])
        f.close()

        files.append(fileName)

    return files

def generatePairs(numberOfPairs: int, stringLength = 0) -> list[list[str]]:
    """ Function to generate pairs of random same length strings\n
    Args:
        numberOfFiles: Number of files to generate
        stringLength: Length of generated strings. Defaults to 0, which makes length random
    Returns:
        List of the generated file pairs
    """

    files = []

    for i in range(numberOfPairs):
        if not stringLength:
            length = random.randint(0, 1000)
        else:
            length = stringLength

        str0 = getRandomString(length)
        str1 = getRandomString(length)

        fileNames = [f"./testFiles/{i}_0.txt", f"./testFiles/{i}_1.txt"]

        f = open(fileNames[0], "w")
        f.write(str0)
        f.close()
        f = open(fileNames[1], "w")
        f.write(str1)
        f.close()

        files.append(fileNames)

    return files


if __name__ == "__main__1":
    # compile c++ executable
    subprocess.run(["make"])

    hashes = []
    totalTime = 0
    totalLength = 0


    for _ in range(1):
        fileName = "test.txt"

        output = subprocess.run(['./main', f"{fileName}"], stdout=subprocess.PIPE)

        result = output.stdout.decode('utf-8').replace("\r", "").split("\n")

        print(result[0])
        hashes.append(result[0])
        totalTime += float(result[1])


    collisions = 0
    hashLengths = 0
    for i in range(len(hashes)):
        collisions += len(findIndices(hashes, hashes[i])) - 1
        hashLengths += len(hashes[i])


    averageCollisions = collisions / len(hashes)
    averageHashLength = hashLengths / len(hashes)
    if averageCollisions != 0:
        print(f"Average collisions: {bcolors.FAIL}{averageCollisions}{bcolors.ENDC}")
    else:
        print(f"Average collisions: {bcolors.OKGREEN}{averageCollisions}{bcolors.ENDC}")
    
    if averageHashLength != 64:
        print(f"Average hash length: {bcolors.FAIL}{averageHashLength}{bcolors.ENDC}")
    else:
        print(f"Average hash length: {bcolors.OKGREEN}{averageHashLength}{bcolors.ENDC}")

    print(f"Average string length: {totalLength / len(hashes)}")
    print(f"Average hashing time: {totalTime / len(hashes)}")

if __name__ == "__main__":
    print(generatePairs(2))