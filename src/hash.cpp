#include "../include/hash.hpp"

std::string Hash::hash(std::string str) {
    std::string key = generateKey(str);

    key += toHex(str);

    return compress(key);
}

std::string Hash::generateKey(std::string str) {
    std::mt19937 mt;
    mt.seed(generateSeed(str));
    std::uniform_int_distribution<int> dist(0, 15);

    std::string output = "";
    for (int i = 0; i < 64; i++) {
        output +=  toHex(dist(mt));
    }

    return output;
}

int Hash::generateSeed(std::string str) {
    std::string bits = toBits(str);
    int seed = bits.length() + toDec(compress(toHex(str), 4));

    for (int i = 0; i < bits.length() / 8; i++) {
        for (int j = 0; j < 8; j++) {
            seed += (j*i) * (char)(bits[i + j]) + j;
        }
    }

    return seed;
}

std::string Hash::compress(std::string hex, int length) {
    while (hex.length() > length) {
        char last = hex.back();
        int index = hex.length() % length;
        
        char newValue = toHex(toDec(last) + toDec(hex[index])).back();
        hex[index] = newValue;

        hex.pop_back();
    }

    return hex;
}

std::string Hash::toHex(std::string str) {
    std::stringstream hex;
    for (char c : str) {
        hex << std::hex << (int)c;
    }

    return hex.str();
}

std::string Hash::toHex(int num) {
    std::stringstream hex;
        hex << std::hex << num;
    return hex.str();
}

std::string Hash::toBits(std::string str) {
    std::stringstream bits;
    for (std::size_t i = 0; i < str.size(); i++) {
        bits << std::bitset<8>(str[i]);
    }
    return bits.str();
}

int Hash::toDec(char c) {
    std::stringstream ss;
    ss << c;
    int y;
    ss >> std::hex >> y;
    return y;
}

int Hash::toDec(std::string str) {
    std::stringstream ss;
    ss << str;
    int y;
    ss >> std::hex >> y;
    return y;
}