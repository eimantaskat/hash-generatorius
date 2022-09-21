import random
import os
import shutil
import string

class TestFiles():
    """ Class to generate test files\n
    Args:
        fileFolder (optional): Path to an empty folder.  Defaults to "./testFiles"

        lowercase (optional): Include lowercase letters in the return list. Defaults to True
        uppercase (optional): Include uppercase letters in the return list. Defaults to True
        digits (optional): Include digits in the return list. Defaults to True
        punctuation (optional): Include punctuation in the return list. Defaults to True
        spaces (optional): Include spaces in the return list. Defaults to True
        newLines (optional): Include new line symbol in the return list. Defaults to True
    """
    def __init__(self, lowercase: bool = True, uppercase: bool = True, digits: bool = True, punctuation: bool = True, spaces: bool = True, newLines: bool = True, fileFolder: str = "./testFiles"):
        self.__fileFolder = fileFolder

        self.allowedCharacters(lowercase=lowercase, uppercase=uppercase, digits=digits, punctuation=punctuation, spaces=spaces, newLines=newLines)

    def setFileFoder(self, path: str):
        """ Function to change test file folder (default "./testFiles")\n
        Args:
            path: Path to an empty folder
        """
        self.__fileFolder = path

    def __clearFolder(self, folder: str):
        """ Function to clear test file folder """
        try:
            for filename in os.listdir(folder):
                filePath = os.path.join(folder, filename)

                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)

        except FileNotFoundError:
            try:
                os.mkdir(folder)
            except FileNotFoundError:
                os.mkdir(self.__fileFolder)
                os.mkdir(folder)

    def allowedCharacters(self, lowercase: bool = None, uppercase: bool = None, digits: bool = None, punctuation: bool = None, spaces: bool = None, newLines: bool = None):
        """ Function to change characters uesd in generated strings\n
        Args:
            lowercase (optional): Include lowercase letters in the return list. Defaults to True
            uppercase (optional): Include uppercase letters in the return list. Defaults to True
            digits (optional): Include digits in the return list. Defaults to True
            punctuation (optional): Include punctuation in the return list. Defaults to True
            spaces (optional): Include spaces in the return list. Defaults to True
            newLines (optional): Include new line symbol in the return list. Defaults to True
        """

        if lowercase != None:
            self.__lowercase = lowercase

        if uppercase != None:
            self.__uppercase = uppercase

        if digits != None:
            self.__digits = digits

        if punctuation != None:
            self.__punctuation = punctuation

        if spaces != None:
            self.__spaces = spaces

        if newLines != None:
            self.__newLines = newLines


    def __getCharacters(self) -> list[str]:
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

        if self.__lowercase:
            characters += list(string.ascii_lowercase)
        if self.__uppercase:
            characters += list(string.ascii_uppercase)
        if self.__digits:
            characters += list(string.digits)
        if self.__punctuation:
            characters += list(string.punctuation)
        if self.__spaces:
            characters += [" "]
        if self.__newLines:
            characters += ["\n"]

        return characters

    def __getRandomString(self, length: int) -> str:
        """ Function that generates random string\n
        Args:
            length: Length of generated string
        Returns:
            Generated string
        """

        characters = self.__getCharacters()
        str = ''.join(random.choice(characters) for _ in range(length))

        return str

    def singleSymbol(self, numberOfFiles: int, existingFiles = False) -> list[str]:
        """ Function to generate text files with one random symbol\n
        Args:
            numberOfFiles: Number of files to generate
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/singleSymbol/"):
                    return [f"{self.__fileFolder}/singleSymbol/{dir}" for dir in os.listdir(f"{self.__fileFolder}/singleSymbol/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/singleSymbol/")

        characters = self.__getCharacters()
        numberOfFiles = len(characters) if numberOfFiles > len(characters) else numberOfFiles

        files = []
        for i in range(numberOfFiles):
            char = random.choice(characters)
            characters.remove(char)

            fileName = f"{self.__fileFolder}/singleSymbol/{i}.txt"

            f = open(fileName, "w")
            f.write(char)
            f.close()

            files.append(fileName)

        return files

    def randomSymbols(self, numberOfFiles: int, numberOfSymbols: int, existingFiles = False) -> list[str]:
        """ Function to generate text files with random symbols\n
        Args:
            numberOfFiles: Number of files to generate
            numberOfSymbols: Number of symbols to generate in every file
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/randomSymbols/"):
                    return [f"{self.__fileFolder}/randomSymbols/{dir}" for dir in os.listdir(f"{self.__fileFolder}/randomSymbols/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/randomSymbols/")
        
        files = []
        for i in range(numberOfFiles):
            str = self.__getRandomString(numberOfSymbols)

            fileName = f"{self.__fileFolder}/randomSymbols/{i}.txt"

            f = open(fileName, "w")
            f.write(str)
            f.close()

            files.append(fileName)

        return files

    def similarSymbols(self, numberOfFiles: int, numberOfSymbols: int, existingFiles = False) -> list[str]:
        """ Function to generate text files with strings that differ from first file by only one symbol\n
        Args:
            numberOfFiles: Number of files to generate
            numberOfSymbols: Number of symbols to generate in every file
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/similarSymbols/"):
                    return [f"{self.__fileFolder}/similarSymbols/{dir}" for dir in os.listdir(f"{self.__fileFolder}/similarSymbols/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/similarSymbols/")
        
        characters = self.__getCharacters()
        baseString = self.__getRandomString(numberOfSymbols)

        if numberOfFiles < 1:
            return []

        files = [f"{self.__fileFolder}/similarSymbols/0.txt"]

        f = open(files[0], "w")
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

            fileName = f"{self.__fileFolder}/similarSymbols/{i}.txt"

            f = open(fileName, "w")
            f.write(str)
            f.close()

            files.append(fileName)

        return files

    def similarPairs(self, numberOfPairs: int, numberOfSymbols: int, existingFiles = False) -> list[str]:
        """ Function to generate pairs of strings that differ by one symbol\n
        Args:
            numberOfPairs: Number of pairs to generate
            stringLength: Length of generated strings. Defaults to 0, which makes length random
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the generated file pairs
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/similarPairs/"):
                    return [f"{self.__fileFolder}/similarPairs/{dir}" for dir in os.listdir(f"{self.__fileFolder}/similarPairs/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/similarPairs/")

        if numberOfPairs < 1:
            return []
        
        characters = self.__getCharacters()


        files = []

        for i in range(0, numberOfPairs):
            baseString = self.__getRandomString(numberOfSymbols)
            str = baseString

            while str == baseString:
                char = random.choice(characters)
                index = random.randint(0, numberOfSymbols - 1)
                str = str[0:index] + char + str[index + 1: ]

            fileNames = [f"{self.__fileFolder}/similarPairs/{i}_0.txt", f"{self.__fileFolder}/similarPairs/{i}_1.txt"]

            f = open(fileNames[0], "w")
            f.write(baseString)
            f.close()

            f = open(fileNames[1], "w")
            f.write(str)
            f.close()

            files.append(fileNames)

        return files

    def emptyFiles(self, numberOfFiles: int, existingFiles = False) -> list[str]:
        """ Function to generate empty text files\n
        Args:
            numberOfFiles: Number of files to generate
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/empty/"):
                    return [f"{self.__fileFolder}/empty/{dir}" for dir in os.listdir(f"{self.__fileFolder}/empty/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/empty/")

        files = []

        for i in range(numberOfFiles):
            fileName = f"{self.__fileFolder}/empty/{i}.txt"

            f = open(fileName, "w")
            f.close() 
        
            files.append(fileName)

        return files

    def generatePairs(self, numberOfPairs: int, stringLength = 0, existingFiles = False) -> list[list[str]]:
        """ Function to generate pairs of random same length strings\n
        Args:
            numberOfPairs: Number of pairs to generate
            stringLength: Length of generated strings. Defaults to 0, which makes length random
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the generated file pairs
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/pairs/"):
                    return [f"{self.__fileFolder}/pairs/{dir}" for dir in os.listdir(f"{self.__fileFolder}/pairs/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/pairs/")
        
        files = []

        for i in range(numberOfPairs):
            if not stringLength:
                length = random.randint(0, 1000)
            else:
                length = stringLength

            str0 = self.__getRandomString(length)
            str1 = self.__getRandomString(length)

            fileNames = [f"{self.__fileFolder}/pairs/{i}_0.txt", f"{self.__fileFolder}/pairs/{i}_1.txt"]

            f = open(fileNames[0], "w")
            f.write(str0)
            f.close()
            f = open(fileNames[1], "w")
            f.write(str1)
            f.close()

            files.append(fileNames[0])
            files.append(fileNames[1])

        return files

    def getLines(self, file = "./konstitucija.txt", existingFiles = False) -> list[str]:
        """ Function to split single text file into files containing one line each\n
        Args:
            file: Path to text file. Defaults to "./konstitucija.txt"
            existingFiles: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of file names with constitution lines
        """

        if existingFiles:
            try:
                if os.listdir(f"{self.__fileFolder}/lines/"):
                    return [f"{self.__fileFolder}/lines/{dir}" for dir in os.listdir(f"{self.__fileFolder}/lines/")]
            except FileNotFoundError:
                pass

        self.__clearFolder(f"{self.__fileFolder}/lines/")

        f = open(file, "r", encoding="utf8")
        lines = f.readlines()

        files = []

        for i in range(len(lines)):
            fileName = f"{self.__fileFolder}/lines/{i}.txt"
            
            f = open(fileName, "w", encoding="utf8")
            f.write(lines[i][0:-1])
            f.close()

            files.append(fileName)

        return files
    
    def getFileList(self, path: str):
        return [f"{path}/{dir}" for dir in os.listdir(path)]