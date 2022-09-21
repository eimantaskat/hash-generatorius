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

int toDec(string c) {
    std::stringstream ss;
    ss << c;
    int y;
    ss >> std::hex >> y;
    return y;
}

string compress(string hex, int length = 64) {
    while (hex.length() > length) {
        char last = hex.back();
        int index = hex.length() % length;
        
        char newValue = toHex(toDec(last) + toDec(hex[index])).back();
        hex[index] = newValue;

        hex.pop_back();
    }

    return hex;
}

int generateSeed(string str) {
    string bits = toBits(str);
    int seed = bits.length() + toDec(compress(toHex(str), 4));

    for (int i = 0; i < bits.length() / 8; i++) {
        for (int j = 0; j < 8; j++) {
            seed += (j*i) * (char)(bits[i + j]) + j;
        }
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
    
    if (argc == 1) {
        cout << "Iveskite teksta\n";
        std::cin >> input;
        cout << hash(input) << "\n";
    } else {
        for (int i = 1; i < argc; i++) {
            input = readFile(argv[1]);
            cout << input << "\n";
            auto start = hrClock::now();
            cout << hash(input) << "\n";
            auto stop = hrClock::now();
            auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start);
            cout << duration.count() * 1e-9 << "\n";
        }
    }
    
    
}