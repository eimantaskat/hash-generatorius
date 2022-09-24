#include "../include/hash.hpp"

#include <iostream>
#include <chrono>
using hrClock = std::chrono::high_resolution_clock;

std::string Hash::hash(std::string str) {
    this->strInput = str;

    this->vectorInput = toCharVector(str);

    std::string k = generateKey(this->vectorInput);

    std::vector<char> key = toCharVector(k);

    std::vector<char> hash;
    hash.reserve(key.size() + this->vectorInput.size());
    hash.insert(hash.end(), key.begin(), key.end());
    hash.insert(hash.end(), this->vectorInput.begin(), this->vectorInput.end());

    return compress(hash);
}

std::vector<char> Hash::toCharVector(std::string str) {
    std::vector<char> v;
    v.reserve(str.length());
    
    for (char c:str) {
        v.push_back(c);
    }
    return v;
}

std::string Hash::generateKey(std::vector<char> str) {
    // auto start = hrClock::now();
    std::mt19937 mt;
    mt.seed(generateSeed(str));
    std::uniform_int_distribution<int> dist(0, 255);

    std::string output = "";
    for (int i = 0; i < 64; i++) {
        output +=  toHex(dist(mt));
    }

    // auto stop = hrClock::now();
    // auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
    // std::cout << "generate key: " << duration.count() * 1e-9 << "\n";

    return output;
}

int Hash::generateSeed(std::vector<char> v) {
    // auto start = hrClock::now();

    int asciiVal = 0;
    for (int i = 0; i < v.size(); i++) {
        asciiVal += i ^ v[i];
    }

    int seed = (v.size() << asciiVal) ^ asciiVal;

    std::string hex = toHex(this->strInput);
    int hexVal = 0;
    for (int i = 0; i < hex.length(); i++) {
        hexVal += i << hex[i];
    }

    seed += toDec(compress(this->vectorInput, 4)) + hexVal;

    // auto stop = hrClock::now();
    // auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
    // std::cout << "generate seed: " << duration.count() * 1e-9 << "\n";
    // std::cout << seed << "\n";
    return seed;
}

std::string Hash::compress(std::vector<char> hex, int length) {
    // auto start = hrClock::now();

    // for (char c:hex)
    //     std::cout << c;
    // std::cout << "\n";

    while (hex.size() > length) {
        char last = hex.back();
        int index = hex.size() % length;
        
        char newValue = last + hex[index];
        hex[index] = newValue;

        hex.pop_back();
    }

    // for (int c:hex) {
    //     std::cout << abs(c) << " ";
    // }
    // std::cout << "\n";

    std::stringstream ss;
    for (char c:hex)
        ss << std::hex << abs(c % 16) << "";
    std::string s = ss.str();

    // auto stop = hrClock::now();
    // auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
    // std::cout << "compress: " << duration.count() * 1e-9 << "\n";

    return s;
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
    for (int i = 0; i < str.size(); i++) {
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