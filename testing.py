import math
from re import M
import subprocess
import string
from more_itertools import locate
from multiprocessing import Pool
import time

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

def similarity(str1: string, str2: string):
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
    filesOneSymbol = filegen.singleSymbol(5, existingFiles = True)
    filesRandSymbols = filegen.randomSymbols(5, 10000, existingFiles = True)
    filesSimSymbols = filegen.similarSymbols(5, 10000, existingFiles = True)
    emptyFiles = filegen.emptyFiles(5, existingFiles = True)

    for files in [filesOneSymbol, filesRandSymbols, filesSimSymbols, emptyFiles]:
        results1 = []
        results2 = []
        
        results1 = hash(files)

        results2 = hash(files)

        printHashes(results1, results2)
        print()

def secondTest(filegen):
    filesConstitution = filegen.getLines("konstitucija.txt")

    results = hash(filesConstitution)

    analyse(results)

def thirdTest(filegen):
    collisions = 0

    pairs_10 = filegen.getFileList("testFiles/pairs_10")
    pairs_100 = filegen.getFileList("testFiles/pairs_100")
    pairs_500 = filegen.getFileList("testFiles/pairs_500")
    pairs_1000 = filegen.getFileList("testFiles/pairs_1000")

    testFiles = pairs_10 + pairs_100 + pairs_500 + pairs_1000

    filesPerChunk = 500

    l = len(testFiles)
    chunkSize = math.ceil(l / (l / filesPerChunk))

    chunks = [testFiles[x:x + chunkSize] for x in range(0, len(testFiles), chunkSize)]

    for chunk in chunks:
        results = hash(chunk)
        for i in range(0, len(results), 2):
            hashes += 2
            if collision(results[i], results[i + 1]):
                collisions += 1

    print(f"Number of collisions: {collisions}")


def fourthTest(filegen):
    files = 0
    hexSimillarity = 0
    maxHex = 0
    minHex = 100

    bitsSimillarity = 0
    maxBits = 0
    minBits = 100
    
    pairs_10 = filegen.getFileList("testFiles/similarPairs_10")
    pairs_100 = filegen.getFileList("testFiles/similarPairs_100")
    pairs_500 = filegen.getFileList("testFiles/similarPairs_500")
    pairs_1000 = filegen.getFileList("testFiles/similarPairs_1000")

    testFiles = pairs_10 + pairs_100 + pairs_500 + pairs_1000

    filesPerChunk = 500

    l = len(testFiles)
    chunkSize = math.ceil(l / (l / filesPerChunk))

    chunks = [testFiles[x:x + chunkSize] for x in range(0, len(testFiles), chunkSize)]

    for chunk in chunks:
        results = hash(chunk)
        for i in range(0, len(results), 2):
            files += 2
            
            hash1 = results[i]["hash"]
            hash2 = results[i + 1]["hash"]
            sim = similarity(hash1, hash2) * 100

            if maxHex < sim:
                maxHex = sim
            if minHex > sim:
                minHex = sim

            hexSimillarity += sim

            hash1Binary = str(bin(int(hash1, 16))[2:]).rjust(256, "0")
            hash2Binary = str(bin(int(hash2, 16))[2:]).rjust(256, "0")
            
            sim = similarity(hash1Binary, hash2Binary) * 100

            if maxBits < sim:
                maxBits = sim
            if minBits > sim:
                minBits = sim

            bitsSimillarity += sim
    
    print(f"Average hex simillarity: {round(hexSimillarity / len(testFiles), 5)}%")
    print(f"Min hex simillarity: {round(minHex, 5)}%")
    print(f"Max hex simillarity: {round(maxHex, 5)}%")
    print()
    print(f"Average bits simillarity: {round(bitsSimillarity / len(testFiles), 5)}%")
    print(f"Min bits simillarity: {round(minBits, 5)}%")
    print(f"Max bits simillarity: {round(maxBits, 5)}%")

def hash(file):
    command = "./main " + " ".join(file)

    output = subprocess.run(command, stdout=subprocess.PIPE)
    output = output.stdout.decode('utf-8').replace("\r", "").split("\n")[0:-1]

    results = []
    for i in range(0, len(output), 3):
        result = {
            "input" :output[i],
            "hash": output[i+1],
            "time": float(output[i+2])
        }
        results.append(result)

    return results

def main():
    filegen = TestFiles(newLines=False, punctuation=False)

    # firstTest(filegen)
    # secondTest(filegen)
    # thirdTest(filegen)
    fourthTest(filegen)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))