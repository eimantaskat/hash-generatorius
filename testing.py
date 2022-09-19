import subprocess
import string
from more_itertools import locate
from difflib import SequenceMatcher

from testFiles import TestFiles

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

# class HashTest

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

if __name__ == "__main__":
    # files = randomSymbols(10, 200)
    filegen = TestFiles()
    print(filegen.emptyFile(2))

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