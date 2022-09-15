#include "main.hpp"

// #include "hash/hash.hpp"

string toHex(string str) {
    std::stringstream hex;
    for (char c : str) {
        hex << std::hex << (int)c;
    }

    return hex.str();
}

string toHex(int str) {
    std::stringstream hex;
        hex << std::hex << str;
    return hex.str();
}

string toBits(string str) {
    std::stringstream bits;
    for (std::size_t i = 0; i < str.size(); i++) {
        bits << std::bitset<8>(str[i]);
    }
    return bits.str();
}

int generateSeed(string str) {
    string bits = toBits(str);
    int seed = bits.length();

    for (int i = 0; i <= bits.length(); i++) {
        seed += i * (char)(bits[i]);
    }

    return seed;
}

string secretKey(string str) {
    std::mt19937 mt;
    mt.seed(static_cast<long unsigned int>(generateSeed(str)));
    std::uniform_int_distribution<int> dist(0, 15);

    string output = "";
    for (int i = 0; i < 64; i++) {
        output +=  toHex(dist(mt));
    }

    return output;
}

string hash(string str) {
    string key = secretKey(str);

    string output = "";

    return output;
}

int main() {
    string in = "Labas";
    // hash(in);
    // cout << hash(in) << " " << hash(in).length();

    cout << secretKey("asdfg") << "\n";
    cout << secretKey("bsdfg") << "\n";
}