import random
import os
import shutil
import string

class Filegen():
    """ Class to generate test files\n
    Args:
        file_folder (optional): Path to an empty folder.  Defaults to "./test_files"

        lowercase (optional): Include lowercase letters in the return list. Defaults to True
        uppercase (optional): Include uppercase letters in the return list. Defaults to True
        digits (optional): Include digits in the return list. Defaults to True
        punctuation (optional): Include punctuation in the return list. Defaults to True
        spaces (optional): Include spaces in the return list. Defaults to True
        new_lines (optional): Include new line symbol in the return list. Defaults to True
    """
    def __init__(self, lowercase: bool = True, uppercase: bool = True, digits: bool = True, punctuation: bool = True, spaces: bool = True, new_lines: bool = True, file_folder: str = "./test_files"):
        self.__file_folder = file_folder

        self.allowed_chars(lowercase=lowercase, uppercase=uppercase, digits=digits, punctuation=punctuation, spaces=spaces, new_lines=new_lines)

    def set_file_folder(self, path: str):
        """ Function to change test file folder (default "./test_files")\n
        Args:
            path: Path to an empty folder
        """
        self.__file_folder = path

    def __clear_folder(self, folder: str):
        """ Function to clear test file folder """
        try:
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)

                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

        except FileNotFoundError:
            try:
                os.mkdir(folder)
            except FileNotFoundError:
                os.mkdir(self.__file_folder)
                os.mkdir(folder)

    def allowed_chars(self, lowercase: bool = None, uppercase: bool = None, digits: bool = None, punctuation: bool = None, spaces: bool = None, new_lines: bool = None):
        """ Function to change characters used in generated strings\n
        Args:
            lowercase (optional): Include lowercase letters in the return list. Defaults to True
            uppercase (optional): Include uppercase letters in the return list. Defaults to True
            digits (optional): Include digits in the return list. Defaults to True
            punctuation (optional): Include punctuation in the return list. Defaults to True
            spaces (optional): Include spaces in the return list. Defaults to True
            new_lines (optional): Include new line symbol in the return list. Defaults to True
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

        if new_lines != None:
            self.__new_lines = new_lines


    def __get_chars(self) -> list[str]:
        """ Function that returns a list of characters\n
        Args:
            lowercase: Include lowercase letters in the return list. Defaults to True
            uppercase: Include uppercase letters in the return list. Defaults to True
            digits: Include digits in the return list. Defaults to True
            punctuation: Include punctuation in the return list. Defaults to True
            spaces: Include spaces in the return list. Defaults to True
            new_lines: Include new line symbol in the return list. Defaults to True
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
        if self.__new_lines:
            characters += ["\n"]

        return characters

    def __random_str(self, length: int) -> str:
        """ Function that generates random string\n
        Args:
            length: Length of generated string
        Returns:
            Generated string
        """

        characters = self.__get_chars()
        str = ''.join(random.choice(characters) for _ in range(length))

        return str

    def generate_one_symbol(self, num_of_files: int, keep_existing = False) -> list[str]:
        """ Function to generate text files with one random symbol\n
        Args:
            num_of_files: Number of files to generate
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if keep_existing:
            try:
                if os.listdir(f"{self.__file_folder}/one_symbol/"):
                    return [f"{self.__file_folder}/one_symbol/{dir}" for dir in os.listdir(f"{self.__file_folder}/one_symbol/")]
            except FileNotFoundError:
                pass

        self.__clear_folder(f"{self.__file_folder}/one_symbol/")

        characters = self.__get_chars()
        num_of_files = len(characters) if num_of_files > len(characters) else num_of_files

        files = []
        for i in range(num_of_files):
            char = random.choice(characters)
            characters.remove(char)

            file_name = f"{self.__file_folder}/one_symbol/{i}.txt"

            f = open(file_name, "w")
            f.write(char)
            f.close()

            files.append(file_name)

        return files

    def generate_random_symbols(self, num_of_files: int, num_of_symbols: int, keep_existing = False) -> list[str]:
        """ Function to generate text files with random symbols\n
        Args:
            num_of_files: Number of files to generate
            num_of_symbols: Number of symbols to generate in every file
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if keep_existing:
            try:
                if os.listdir(f"{self.__file_folder}/random_symbols/"):
                    return [f"{self.__file_folder}/random_symbols/{dir}" for dir in os.listdir(f"{self.__file_folder}/random_symbols/")]
            except FileNotFoundError:
                pass

        self.__clear_folder(f"{self.__file_folder}/random_symbols/")
        
        files = []
        for i in range(num_of_files):
            str = self.__random_str(num_of_symbols)

            file_name = f"{self.__file_folder}/random_symbols/{i}.txt"

            f = open(file_name, "w")
            f.write(str)
            f.close()

            files.append(file_name)

        return files

    def generate_simillar_symbols(self, num_of_files: int, num_of_symbols: int, keep_existing = False) -> list[str]:
        """ Function to generate text files with strings that differ from first file by only one symbol\n
        Args:
            num_of_files: Number of files to generate
            num_of_symbols: Number of symbols to generate in every file
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if keep_existing:
            try:
                if os.listdir(f"{self.__file_folder}/simillar_symbols/"):
                    return [f"{self.__file_folder}/simillar_symbols/{dir}" for dir in os.listdir(f"{self.__file_folder}/simillar_symbols/")]
            except FileNotFoundError:
                pass

        self.__clear_folder(f"{self.__file_folder}/simillar_symbols/")
        
        characters = self.__get_chars()
        base_string = self.__random_str(num_of_symbols)

        if num_of_files < 1:
            return []

        files = [f"{self.__file_folder}/simillar_symbols/0.txt"]

        f = open(files[0], "w")
        f.write(base_string)
        f.close()

        generated = []

        for i in range(1, num_of_files):
            str = base_string

            while str == base_string or (str in generated):
                char = random.choice(characters)
                index = random.randint(0, num_of_symbols - 1)
                str = str[0:index] + char + str[index + 1: ]

            generated.append(str)

            file_name = f"{self.__file_folder}/simillar_symbols/{i}.txt"

            f = open(file_name, "w")
            f.write(str)
            f.close()

            files.append(file_name)

        return files

    def generate_similar_pairs(self, number_of_pairs: int, string_length: int, keep_existing = False) -> list[str]:
        """ Function to generate pairs of strings that differ by one symbol\n
        Args:
            number_of_pairs: Number of pairs to generate
            string_length: Length of generated strings. Defaults to 0, which makes length random
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the generated file pairs
        """

        file_name = f"{self.__file_folder}/similar_pairs/{string_length}.txt"


        if keep_existing:
            if os.path.exists(file_name):
                return file_name
        
        characters = self.__get_chars()

        f = open(file_name, "w")

        for i in range(0, number_of_pairs):
            if i != 0:
                f.write("\n")
                
            base_str = self.__random_str(string_length)
            str = base_str

            while str == base_str:
                char = random.choice(characters)
                index = random.randint(0, string_length - 1)
                str = str[0:index] + char + str[index + 1: ]

            f.write(base_str + "\n")
            f.write(str)

        f.close()

        return file_name

    def generate_empty_files(self, num_of_files: int, keep_existing = False) -> list[str]:
        """ Function to generate empty text files\n
        Args:
            num_of_files: Number of files to generate
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the names of generated files
        """

        if keep_existing:
            try:
                if os.listdir(f"{self.__file_folder}/empty/"):
                    return [f"{self.__file_folder}/empty/{dir}" for dir in os.listdir(f"{self.__file_folder}/empty/")]
            except FileNotFoundError:
                pass

        self.__clear_folder(f"{self.__file_folder}/empty/")

        files = []

        for i in range(num_of_files):
            file_name = f"{self.__file_folder}/empty/{i}.txt"

            f = open(file_name, "w")
            f.close() 
        
            files.append(file_name)

        return files

    def generate_pairs(self, number_of_pairs: int, string_length = 0, keep_existing = False) -> list[list[str]]:
        """ Function to generate strings pairs of random length\n
        Args:
            number_of_pairs: Number of pairs to generate
            string_length: Length of generated strings. Defaults to 0, which makes length random
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of the generated file pairs
        """

        file_name = f"{self.__file_folder}/pairs/{string_length}.txt"

        if keep_existing:
            if os.path.exists(file_name):
                return file_name
        
        f = open(file_name, "w")

        for i in range(number_of_pairs):
            if i != 0:
                f.write("\n")

            if not string_length:
                length = random.randint(0, 1000)
            else:
                length = string_length

            str0 = self.__random_str(length)
            str1 = self.__random_str(length)


            f.write(str0 + "\n")
            f.write(str1)

        f.close()

        return file_name

    def get_lines(self, file = "./konstitucija.txt", keep_existing = False) -> list[str]:
        """ Function to split single text file into files containing one line each\n
        Args:
            file: Path to text file. Defaults to "./konstitucija.txt"
            keep_existing: If true, checks for existing files and returns them if found. Defaults to False
        Returns:
            List of file names with constitution lines
        """

        if keep_existing:
            try:
                if os.listdir(f"{self.__file_folder}/lines/"):
                    return [f"{self.__file_folder}/lines/{dir}" for dir in os.listdir(f"{self.__file_folder}/lines/")]
            except FileNotFoundError:
                pass

        self.__clear_folder(f"{self.__file_folder}/lines/")

        f = open(file, "r", encoding="utf8")
        lines = f.readlines()

        files = []

        for i in range(len(lines)):
            file_name = f"{self.__file_folder}/lines/{i}.txt"
            
            f = open(file_name, "w", encoding="utf8")
            f.write(lines[i][0:-1])
            f.close()

            files.append(file_name)

        return files
    
    def get_file_list(self, path: str):
        return [f"{path}/{dir}" for dir in os.listdir(path)]