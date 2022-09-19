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
        self.fileFolder = fileFolder

        self.allowedCharacters(lowercase=lowercase, uppercase=uppercase, digits=digits, punctuation=punctuation, spaces=spaces, newLines=newLines)

    def setFileFoder(self, path: str):
        """ Function to change test file folder (default "./testFiles")\n
        Args:
            path: Path to an empty folder
        """
        self.fileFolder = path

    def clearFileFolder(self):
        """ Function to clear test file folder """
        try:
            for filename in os.listdir(self.fileFolder):
                filePath = os.path.join(self.fileFolder, filename)

                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
        except FileNotFoundError:
            os.mkdir(self.fileFolder)

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
            self.lowercase = lowercase

        if uppercase != None:
            self.uppercase = uppercase

        if digits != None:
            self.digits = digits

        if punctuation != None:
            self.punctuation = punctuation

        if spaces != None:
            self.spaces = spaces

        if newLines != None:
            self.newLines = newLines


    def getCharacters(self) -> list[str]:
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

        if self.lowercase:
            characters += list(string.ascii_lowercase)
        if self.uppercase:
            characters += list(string.ascii_uppercase)
        if self.digits:
            characters += list(string.digits)
        if self.punctuation:
            characters += list(string.punctuation)
        if self.spaces:
            characters += [" "]
        if self.newLines:
            characters += ["\n"]

        return characters

    def getRandomString(self, length: int) -> str:
        """ Function that generates random string\n
        Args:
            length: Length of generated string
        Returns:
            Generated string
        """

        characters = self.getCharacters()
        str = ''.join(random.choice(characters) for _ in range(length))

        return str

    def singleSymbol(self, numberOfFiles: int) -> list[str]:
        """ Function to generate text files with one random symbol\n
        Args:
            numberOfFiles: Number of files to generate
        Returns:
            List of the names of generated files
        """
        self.clearFileFolder()

        characters = self.getCharacters()
        numberOfFiles = len(characters) if numberOfFiles > len(characters) else numberOfFiles

        files = []
        for i in range(numberOfFiles):
            char = random.choice(characters)
            characters.remove(char)

            fileName = f"{self.fileFolder}/{i}.txt"

            f = open(fileName, "w")
            f.write(char)
            f.close()

            files.append(fileName)

        return files

    def randomSymbols(self, numberOfFiles: int, numberOfSymbols: int) -> list[str]:
        """ Function to generate text files with random symbols\n
        Args:
            numberOfFiles: Number of files to generate
            numberOfSymbols: Number of symbols to generate in every file
        Returns:
            List of the names of generated files
        """
        self.clearFileFolder()
        
        files = []
        for i in range(numberOfFiles):
            str = self.getRandomString(numberOfSymbols)

            fileName = f"{self.fileFolder}/{i}.txt"

            f = open(fileName, "w")
            f.write(str)
            f.close()

            files.append(fileName)

        return files

    def similarSymbols(self, numberOfFiles: int, numberOfSymbols: int) -> list[str]:
        """ Function to generate text files with strings that differ from first file by only one symbol\n
        Args:
            numberOfFiles: Number of files to generate
            numberOfSymbols: Number of symbols to generate in every file
        Returns:
            List of the names of generated files
        """

        self.clearFileFolder()
        
        characters = self.getCharacters()
        baseString = self.getRandomString(numberOfSymbols)

        if numberOfFiles < 1:
            return []

        files = [f"{self.fileFolder}/0.txt"]

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

            fileName = f"{self.fileFolder}/{i}.txt"

            f = open(fileName, "w")
            f.write(str)
            f.close()

            files.append(fileName)

        return files

    def emptyFile(self, numberOfFiles: int) -> list[str]:
        """ Function to generate empty text files\n
        Args:
            numberOfFiles: Number of files to generate
        Returns:
            List of the names of generated files
        """

        self.clearFileFolder()

        files = []

        for i in range(numberOfFiles):
            fileName = f"{self.fileFolder}/{i}.txt"

            f = open(fileName, "w")
            f.close() 
        
            files.append(fileName)

        return files

    def generatePairs(self, numberOfPairs: int, stringLength = 0) -> list[list[str]]:
        """ Function to generate pairs of random same length strings\n
        Args:
            numberOfPairs: Number of pairs to generate
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

            str0 = self.getRandomString(length)
            str1 = self.getRandomString(length)

            fileNames = [f"{self.fileFolder}/{i}_0.txt", f"{self.fileFolder}/{i}_1.txt"]

            f = open(fileNames[0], "w")
            f.write(str0)
            f.close()
            f = open(fileNames[1], "w")
            f.write(str1)
            f.close()

            files.append(fileNames)

        return files

    def constitutionLines(self, constitutionFile = "./konstitucija.txt") -> list[str]:
        """ Function to get Lithuanian constitution text\n
        Args:
            constitutionFile: Path to text file. Defaults to "./konstitucija.txt"
        Returns:
            List of file names with constitution lines
        """

        f = open(constitutionFile, "r", encoding="utf8")
        lines = f.readlines()

        files = []

        for i in range(len(lines)):
            fileName = f"{self.fileFolder}/{i}.txt"
            
            f = open(fileName, "w", encoding="utf8")
            f.write(lines[i][0:-1])
            f.close()

            files.append(fileName)

        return files