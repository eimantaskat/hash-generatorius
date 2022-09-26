#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <vector>

#include "../include/hash.hpp"
#include "../include/SHA256.hpp"

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

void writeData(std::string out, std::string fileName = "hash_output.txt") {
    std::ofstream file (fileName);
    file << out;
    file.close();
    std::cout << fileName;
}

int main(int argc, char** argv) {
    std::string input;

    Hash h256;

    if (argc == 1) {
        std::cout << "Iveskite teksta\n";
        std::cin >> input;
        std::cout << h256.hash(input) << "\n";
    } else {
        if (std::string(argv[1]) == "--file" || std::string(argv[1]) == "-f") {

            std::stringstream output;

            for (int i = 2; i < argc; i++) {
                input = readFile(argv[i]);
                output << input << "|";

                auto start = hrClock::now();

                std::string hash = h256.hash(input);
                // std::string hash = sha256(input);

                auto stop = hrClock::now();
                auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);

                output << hash << "|";
                output << duration.count() * 1e-9 << "|";
            }

            writeData(output.str());

        } else if (std::string(argv[1]) == "--lines" || std::string(argv[1]) == "-l") {

            std::stringstream output;

            for (int i = 2; i < argc; i++) {
                std::vector<std::string> input = readLines(argv[i]);

                for (std::string line:input) {
                    output << line << "|";
                    auto start = hrClock::now();

                    std::string hash = h256.hash(line);

                    auto stop = hrClock::now();
                    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);

                    output << hash << "|";
                    output << duration.count() * 1e-9 << "|";
                }

            }

            writeData(output.str());

        }
    }
    
    
}