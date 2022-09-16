#include "main.hpp"

// #include "hash/hash.hpp"

string toHex(string str) {
    std::stringstream hex;
    for (char c : str) {
        hex << std::hex << (int)c;
    }

    return hex.str();
}

string toHex(int num) {
    std::stringstream hex;
        hex << std::hex << num;
    return hex.str();
}

string toBits(string str) {
    std::stringstream bits;
    for (std::size_t i = 0; i < str.size(); i++) {
        bits << std::bitset<8>(str[i]);
    }
    return bits.str();
}

int toDec(char c) {
    std::stringstream ss;
    ss << c;
    int y;
    ss >> std::hex >> y;
    return y;
}

int generateSeed(string str) {
    string bits = toBits(str);
    int seed = bits.length();

    for (int i = 0; i <= bits.length(); i++) {
        seed += (i + 1) * (char)(bits[i]);
    }


    return seed;
}

string secretKey(string str) {
    std::mt19937 mt;
    mt.seed(generateSeed(str));
    std::uniform_int_distribution<int> dist(0, 15);

    string output = "";
    for (int i = 0; i < 64; i++) {
        output +=  toHex(dist(mt));
    }

    return output;
}

string compress(string hex) {
    while (hex.length() > 64) {
        char last = hex.back();
        int index = hex.length() % 64;
        
        char newValue = toHex(toDec(last) + toDec(hex[index])).back();
        hex[index] = newValue;

        hex.pop_back();
    }

    return hex;
}

string hash(string str) {
    string key = secretKey(str);

    key += toHex(str);

    return compress(key);
}

string readFile(string fileName) {
    std::ifstream file (fileName);
    std::stringstream buffer;
    buffer << file.rdbuf();
    file.close();

    return buffer.str();
}

int main(int argc, char** argv) {
    string input;

    if (argc > 1)
        input = readFile(argv[1]);
    else {
        // TODO
        // manual input
    }

    auto start = hrClock::now();
    cout << hash(input) << "\n";
    auto stop = hrClock::now();
    auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
    cout << duration.count() * 1e-9 << "";
}