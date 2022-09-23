#pragma once

#include <string>
#include <random>
#include <sstream>
#include <bitset>

class Hash {
    public:
        Hash() {};
        std::string hash(std::string);
    private:
        std::string generateKey(std::string);
        int generateSeed(std::string);

        std::string compress(std::string, int length = 64);

        std::string toHex(std::string);
        std::string toHex(int);
        std::string toBits(std::string);
        int toDec(char);
        int toDec(std::string);
};