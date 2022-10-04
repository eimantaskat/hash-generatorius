#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <ctime>    
#include <vector>
#include <thread>

#include "../include/hash.hpp"

using hrClock = std::chrono::high_resolution_clock;

std::string readFile(std::string fileName) {
    std::ifstream file (fileName);
    std::stringstream buffer;
    buffer << file.rdbuf();
    file.close();

    return buffer.str();
}

std::vector<std::string> readLines(std::string fileName) {
    std::stringstream buffer;

    std::ifstream file(fileName);
    if (!file) {
        throw("Failas neegzistuoja");
    }
    buffer << file.rdbuf();

    file.close();

    int lines_count = 0;
    std::string line;
    while (getline(buffer, line)) {
        lines_count++;
    }

    buffer.clear();
    buffer.seekg(0, std::ios::beg);

    std::vector<std::string> lines;
    lines.reserve(lines_count);
    while (!buffer.eof()) {
        std::string str;
        getline(buffer, str);
        lines.push_back(str);
    }

    return lines;
}

std::string generateSalt(std::string file, Hash &h256) {
    auto n = static_cast<long unsigned int>(hrClock::now().time_since_epoch().count());
    std::string salt = h256.hash(std::to_string(n));
    std::chrono::milliseconds timespan(1);
    std::this_thread::sleep_for(timespan);
    return salt;
}

void unknownOption(std::string option) {
    std::cout << "unknown option: " << option << "\n";
    exit(64);
}

int main(int argc, char** argv) {
    Hash h256;

    std::string input;

    bool useSalt = false;
    std::string salt = "";

    bool files = false;
    bool lines = false;

    int filesBegin = 0;
    int filesEnd = 0;

    // command line argumentų patikrinimas
    for (int i = 0; i < argc; i++) {
        std::string arg = std::string(argv[i]);

        // jei ne command line argumentas, praleisti
        if (arg.front() != '-')
            continue;

        if (arg == "-s") {
            useSalt = true;
            filesEnd = i;
        } else if (arg.substr(0, 7) == "--salt=") {
            useSalt = true;
            salt = arg.substr(7, arg.length() - 1);
            filesEnd = i;
        } else if (arg == "-f" || arg == "--file") {
            files = true;
            filesBegin = i+1;
        } else if (arg == "-l" || arg == "--lines") {
            lines = true;
            filesBegin = i+1;
        } else {
            unknownOption(arg);
        }
    }

    if (filesBegin > filesEnd)
        filesEnd = argc;

    // rankinis duomenų įvedimas

    // be salt
    if (!files && !lines && !useSalt) {
        std::cout << "Norint uzdaryti programa spauskite ctrl + c\n";
        while (true) {
            std::cout << "Iveskite teksta: ";
            std::cin >> input;
            std::cout << h256.hash(input) << "\n";
        }
    }

    // su salt
    if (!files && !lines && useSalt) {
        std::cout << "Norint uzdaryti programa spauskite ctrl + c\n";
        while (true) {
            std::cout << "Iveskite teksta: ";
            std::cin >> input;

            if (salt.length() == 0) {
                std::cout << "Iveskite salt: ";
                std::cin >> salt;
            }

            std::cout << h256.hashWithSalt(input, salt) << "\n";
        }
    }

    // duomenys iš failų

    // viso failo hashinimas be salt
    if (files && !useSalt) {
        for (int i = filesBegin; i < filesEnd; i++) {
            input = readFile(argv[i]);
            std::cout << input << ": ";

            std::string hash = h256.hash(input);

            std::cout << hash << "\n";
        }
        return 0;
    }

    // viso failo hashinimas su salt
    if (files && useSalt) {
        for (int i = filesBegin; i < filesEnd; i++) {
            input = readFile(argv[i]);
            std::cout << input << ": ";

            std::string s = salt;

            if (salt.length() == 0) {
                salt = generateSalt(argv[i], h256);
            }

            std::string hash = h256.hashWithSalt(input, salt);

            std::cout << hash << " (salt: " << salt << ")\n";
            salt = s;
        }
        return 0;
    }
    
    // kiekvienos failo eitutės hashinimas be salt
    if (lines && !useSalt) {
        for (int i = filesBegin; i < filesEnd; i++) {
            std::vector<std::string> input = readLines(argv[i]);

            for (std::string line:input) {
                std::cout << line << ": ";

                std::string hash = h256.hash(line);

                std::cout << hash << "\n";
            }
        }
        return 0;
    }

    // kiekvienos failo eitutės hashinimas su salt
    if (lines && useSalt) {
        for (int i = filesBegin; i < filesEnd; i++) {
            std::vector<std::string> input = readLines(argv[i]);

            for (std::string line:input) {
                std::cout << line << ": ";

                std::string s = salt;

                if (salt.length() == 0) {
                    salt = generateSalt(argv[i], h256);
                }

                std::string hash = h256.hashWithSalt(line, salt);

                std::cout << hash << " (salt: " << salt << ")\n";
                salt = s;
            }
        }
        return 0;
    }
}