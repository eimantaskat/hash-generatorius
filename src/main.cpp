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

int main(int argc, char** argv) {
    std::string input;

    Hash h256;
    
    // input = readFile("konstitucija.txt");
    // auto start = hrClock::now();
    // std::string hash = h256.hash(input);
    // // std::string hash = sha256(input);
    // auto stop = hrClock::now();
    // std::cout << hash << "\n";
    // auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
    // std::cout << duration.count() * 1e-9 << "\n";


    if (argc == 1) {
        std::cout << "Iveskite teksta\n";
        std::cin >> input;
        std::cout << h256.hash(input) << "\n";
    } else {
        for (int i = 1; i < argc; i++) {
            input = readFile(argv[i]);
            // input = readFile("konstitucija.txt");
            std::cout << input << "|";

            auto start = hrClock::now();
            // std::string hash = h256.hash(input);
            std::string hash = sha256(input);
            auto stop = hrClock::now();

            std::cout << hash << "|";
            auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
            std::cout << duration.count() * 1e-9 << "|";
        }
    }
    
    
}