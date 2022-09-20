import re
import subprocess
import string
from more_itertools import locate
from multiprocessing import Pool
import time
import binascii

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

    matchingSymbols = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            matchingSymbols += 1

    return matchingSymbols / len(str1)

def collision(res1, res2):
    if res1["hash"] != res2["hash"]:
        return False
    elif res1["input"] == res2["input"]:
        return False
    return True

def analyse(hashes):
    totalHashes = len(hashes)

    totalTime = 0
    minTime = hashes[0]["time"]
    maxTime = hashes[0]["time"]
    
    totalInputLength = 0
    totalHashLength = 0

    collisions = 0

    for i in range(len(hashes)):
        totalTime += hashes[i]["time"]

        if hashes[i]["time"] > maxTime:
            maxTime = hashes[i]["time"]

        if hashes[i]["time"] < minTime:
            minTime = hashes[i]["time"]

        totalInputLength += len(hashes[i]["input"])
        totalHashLength += len(hashes[i]["hash"])

        for j in range(i, len(hashes)):
            if collision(hashes[i], hashes[j]):
                collisions += 1

    print(f"Hashed {totalHashes} strings ({totalInputLength} symbols) in {round(totalTime, 5)}s")
    print(f"Average hash time: {round(totalTime / totalHashes, 5)}s")
    print(f"Max hash time: {round(maxTime, 5)}s")
    print(f"Min hash time: {round(minTime, 5)}s")

    print(f"Average input length: {round(totalInputLength / totalHashes, 5)}")
    print(f"Average hash length: {bcolors.OKGREEN if totalHashLength / totalHashes == 64 else bcolors.FAIL}{totalHashLength / totalHashes}{bcolors.ENDC}")
    print(f"Collisions: {bcolors.OKGREEN if collisions == 0 else bcolors.FAIL}{collisions}{bcolors.ENDC}")

def hash(file):
    output = subprocess.run(['./main', f"{file}"], stdout=subprocess.PIPE)
    output = output.stdout.decode('utf-8').replace("\r", "").split("\n")

    result = {
        "input": output[0],
        "hash": output[1],
        "time": float(output[2])
    }
    return result

def parallerHash(files, poolSize):
    results = []

    with Pool(poolSize) as pool:
        result = pool.map_async(hash, files)
        results += result.get()

    return results

def printHashes(results):
    for result in results:
        print(result["hash"])

def printHashes(results0, results1):
    for i in range(len(results0)):
        print(results0[i]["hash"], results1[i]["hash"])

def firstTest(filegen):
    filesOneSymbol = filegen.singleSymbol(5)
    filesRandSymbols = filegen.randomSymbols(5, 10000)
    filesSimSymbols = filegen.similarSymbols(5, 10000)
    emptyFiles = filegen.emptyFile(5)

    for files in [filesOneSymbol, filesRandSymbols, filesSimSymbols, emptyFiles]:
        results1 = []
        results2 = []
        with Pool(1) as pool:
            result = pool.map_async(hash, files)
            results1 += result.get()

        with Pool(1) as pool:
            result = pool.map_async(hash, files)
            results2 += result.get()

        printHashes(results1, results2)
        print()

def secondTest(filegen):
    filesConstitution = filegen.getLines("konstitucija.txt")
    
    results = parallerHash(filesConstitution, 1)

    analyse(results)

def thirdTest(filegen):
    collisions = 0

    for symbols in [10, 100, 500, 1000]:
        filesSymbolPairs = filegen.generatePairs(25000, symbols)
        for pair in filesSymbolPairs:
            results = parallerHash(pair, 8)
            if collision(results[0], results[1]):
                collisions += 1

    print(f"Number of collisions: {collisions}")

def fourthTest(filegen):
    hexSimillarity = 0
    bitsSimillarity = 0
    pairs = 20

    for symbols in [10, 100, 500, 1000]:
        filesSymbolPairs = filegen.similarPairs(pairs // 4, symbols)
        for pair in filesSymbolPairs:
            results = parallerHash(pair, 8)
            hash1 = results[0]["hash"]
            hash2 = results[1]["hash"]
            hexSimillarity += similarity(hash1, hash2)

            
            hash1Binary = str(bin(int(hash1, 16))[2:])
            hash2Binary = str(bin(int(hash2, 16))[2:])
            print(len(hash2Binary), len(hash1Binary))
            # bitsSimillarity += similarity(hash1Binary, hash2Binary)
    
    print(f"Hex simillarity: {round(hexSimillarity / pairs * 100, 5)}%")
    print(f"Bits simillarity: {round(bitsSimillarity / pairs * 100, 5)}%")

def main():
    filegen = TestFiles(newLines=False)

    # firstTest(filegen)
    # secondTest(filegen)
    # thirdTest(filegen)
    fourthTest(filegen)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))