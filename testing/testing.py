import os
import subprocess
import string
import time

from Filegen import Filegen

def similarity(str1: string, str2: string):
    matching_symbols = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            matching_symbols += 1

    return matching_symbols / len(str1)

def collision(res1, res2):
    if res1["hash"] != res2["hash"]:
        return False
    elif res1["input"] == res2["input"]:
        return False
    return True

def analyse(hashes, time = True, length = True, collisions = True, type = "simbolių eillučių", amount = -1):
    total_hashes = len(hashes)

    total_time = 0
    if time:
        min_time = hashes[0]["time"]
        max_time = hashes[0]["time"]
    
    total_input_length = 0
    if length:
        total_hash_length = 0

    if collisions:
        colls = 0 # collisions

    for i in range(len(hashes)):
        total_time += hashes[i]["time"]
        if time:

            if hashes[i]["time"] > max_time:
                max_time = hashes[i]["time"]

            if hashes[i]["time"] < min_time:
                min_time = hashes[i]["time"]

        total_input_length += len(hashes[i]["input"])
        if length:
            total_hash_length += len(hashes[i]["hash"])

        if collisions:
            for j in range(i, len(hashes)):
                if collision(hashes[i], hashes[j]):
                    colls += 1

    print(f"Suhash'inta {total_hashes if amount == -1 else amount} {type} ({total_input_length} simbolių) per {total_time:.5f}s")
    if time:
        print(f"Vidutinis hash'avimo laikas: {(total_time / total_hashes):.5f}s")
        print(f"Didžiausias hash'avimo laikas: {max_time:.5f}s")
        print(f"Mažiausias hash'avimo laikas: {min_time:.5f}s")

    if length:
        print(f"Vidutinis input'o ilgis: {(total_input_length / total_hashes):.5f}")
        print(f"Vidutinis hash'o ilgis: {total_hash_length / total_hashes}")
    
    if collisions:
        print(f"Kolizijos: {colls}")

def print_hashes(results):
    for result in results:
        print(result["hash"])

def print_hashes(results1, results2):
    for i in range(len(results1)):
        print(results1[i]["hash"], results2[i]["hash"])

def test_1(fg, regen_files = False):
    one_symbol_f = fg.generate_one_symbol(2, keep_existing = not regen_files)
    rand_symbols_f = fg.generate_random_symbols(2, 10000, keep_existing = not regen_files)
    sim_symbols_f = fg.generate_simillar_symbols(2, 10000, keep_existing = not regen_files)
    empty_f = fg.generate_empty_files(2, keep_existing = not regen_files)

    print(f"Pirmas hash'avimas{' ' * 47}Antras hash'avimas")

    for files in [one_symbol_f, rand_symbols_f, sim_symbols_f, empty_f]:
        if files == one_symbol_f:
            print("Inputa'ai - failai su vienu simboliu:")
        elif files == rand_symbols_f:
            print("\nInputa'ai - failai su 10 000 atsitiktinių simbolių:")
        elif files == sim_symbols_f:
            print("\nInputa'ai - 10 000 simbolių failai, kurie skiriasi nuo pirmo failo vienu simboliu:")
        elif files == empty_f:
            print("\nInputa'ai - tušti failai:")
        results1 = []
        results2 = []
        
        results1 = hash(files, "-f")

        results2 = hash(files, "-f")

        print_hashes(results1, results2)

def test_2(fg, regen_files = False):
    times = []
    passes = 20

    f = "konstitucija.txt"

    file = open(f, encoding="utf8")
    lines = file.readlines()
    file.close()

    indexes = []

    i = 1
    while i < len(lines):
        indexes.append(i) 
        i *= 2

    indexes.append(len(lines))


    for _ in range(passes):
        time = []
        for i in indexes:
            tmp_f = open("tmp.txt", "w", encoding="utf8")
            tmp_f.write("".join(lines[0:i])[0:-1])
            tmp_f.close()

            results = hash(["tmp.txt"], "-f")
            time.append(results[0]["time"])

        times.append(time)
            
    times = [sum(x) for x in zip(*times)]

    print(f"{passes} hash'avimų vidurkis:")
    for i in range(len(indexes)):
        print(f"{indexes[i]} eilutės: {times[i] / passes:.5f}s")

def test_3(fg, regen_files = False):
    collisions = 0
    results = []

    pairs_10 = fg.generate_pairs(25000, 10, keep_existing = not regen_files)
    pairs_100 = fg.generate_pairs(25000, 100, keep_existing = not regen_files)
    pairs_500 = fg.generate_pairs(25000, 500, keep_existing = not regen_files)
    pairs_1000 = fg.generate_pairs(25000, 1000, keep_existing = not regen_files)

    f = [pairs_10, pairs_100, pairs_500, pairs_1000]

    results = hash(f, "-l")
    for i in range(0, len(results), 2):
        if collision(results[i], results[i + 1]):
            collisions += 1

    analyse(results, collisions=False)
    print(f"Kolizijos: {collisions}")


def test_4(fg, regen_files = False):
    results = []

    hex_simillarity = 0
    max_hex = 0
    min_hex = 100

    bits_simillarity = 0
    max_bits = 0
    min_bits = 100
    
    pairs_10 = fg.generate_similar_pairs(25000, 10, keep_existing = not regen_files)
    pairs_100 = fg.generate_similar_pairs(25000, 100, keep_existing = not regen_files)
    pairs_500 = fg.generate_similar_pairs(25000, 500, keep_existing = not regen_files)
    pairs_1000 = fg.generate_similar_pairs(25000, 1000, keep_existing = not regen_files)

    f = [pairs_10, pairs_100, pairs_500, pairs_1000]

    results = hash(f, "-l")

    s = 0
    for i in range(0, len(results), 2):          
        hash1 = results[i]["hash"]
        hash2 = results[i + 1]["hash"]
        sim = similarity(hash1, hash2) * 100

        if max_hex < sim:
            max_hex = sim
        if min_hex > sim:
            min_hex = sim

        hex_simillarity += sim

        hash1_binary = str(bin(int(hash1, 16))[2:]).rjust(256, "0")
        hash2_binary = str(bin(int(hash2, 16))[2:]).rjust(256, "0")
        
        sim = similarity(hash1_binary, hash2_binary) * 100

        if max_bits < sim:
            max_bits = sim
        if min_bits > sim:
            min_bits = sim

        bits_simillarity += sim

    #     if sim == 100:
    #         # print(results[i], results[i+1])
    #         s += 1
    # print(f"{s = }")
    
    analyse(results, collisions=False)
    print()
    print(f"Vidutinis hex'ų panašumas: {(hex_simillarity / len(results)):.5f}%")
    print(f"Mažiausias hex'ų panašumas: {min_hex:.2f}%")
    print(f"Didžiausias hex'ų panašumas: {max_hex:.2f}%")
    print()
    print(f"Vidutinis bitų panašumas: {(bits_simillarity / len(results)):.5f}%")
    print(f"Mažiausias bitų panašumas: {min_bits:.2f}%")
    print(f"Didžiausias bitų panašumas: {max_bits:.2f}%")

def hash(file, flag):
    command = "./hash-test " + flag + " " + " ".join(file)

    output = subprocess.run(command, stdout=subprocess.PIPE)
    output_file = output.stdout.decode('utf-8')

    results = []

    file = open(output_file, "r", encoding="utf8")
    output = file.read().split("|")[0:-1]
    file.close()

    for i in range(0, len(output), 3):
        result = {
            "input": output[i],
            "hash": output[i + 1],
            "time": float(output[i + 2])
        }
        results.append(result)

    return results

def main():
    fg = Filegen(new_lines=False, punctuation=False, file_folder="./test_files")
    regen_files = False

    print("--- Output'ų dydžio, to paties failo hash'o testavimas ---")
    test_1(fg, regen_files)

    print("\n--- Hash funkcijos efektyvumo testavimas: kostitucijos eilučių hash'avimas ---")
    test_2(fg, regen_files)

    print("\n--- Atsparumo kolizijai testavimas: 25 000 porų po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---")
    test_3(fg, regen_files)

    print("\n--- Lavinos efekto testavimas: 25 000 porų (poros simbolių eilutės skiriasi 1 simboliu), po 10, 100, 500 ir 1 000 atsitiktinių simbolių hash'inimas ---")
    test_4(fg, regen_files)

    os.remove("hash_output.txt")
    os.remove("tmp.txt")
    os.remove("hash-test.exe")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- Testavimas baigtas per {(time.time() - start_time):.2f} s ---")