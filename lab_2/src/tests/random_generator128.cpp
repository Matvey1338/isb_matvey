#include <iostream>
#include <random>
#include <bitset>
#include <string>
#include <locale>

class RandomGenerator128 {
private:
    std::random_device rd;
    std::mt19937_64 gen;
    uint64_t high_bits;
    uint64_t low_bits;

public:
    RandomGenerator128() : gen(rd()) {
        generate();
    }

    void generate() {
        high_bits = gen();
        low_bits = gen();
    }

    std::string get_binary_string() const {
        std::bitset<64> hi(high_bits), lo(low_bits);
        return hi.to_string() + lo.to_string();
    }

    void print_binary() const {
        std::cout << get_binary_string() << std::endl;
    }

    void count_bits() const {
        std::string binary = get_binary_string();
        int zeros = 0;
        int ones = 0;
        
        for (char bit : binary) {
            if (bit == '0') zeros++;
            else ones++;
        }
        
        std::cout << "Количество нулей: " << zeros << std::endl;
        std::cout << "Количество единиц: " << ones << std::endl;
    }
};

int main() {
    // Установка русской локали
    setlocale(LC_ALL, "ru_RU.UTF-8");

    RandomGenerator128 generator;
    std::cout << "Сгенерированное число в двоичном виде:" << std::endl;
    generator.print_binary();
    generator.count_bits();
    
    return 0;
}