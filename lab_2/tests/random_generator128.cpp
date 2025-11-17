#include <iostream>
#include <random>
#include <bitset>
#include <string>
#include <locale>

/**
 * @brief Генератор случайных 128-битных чисел
 * 
 * Класс для генерации и анализа 128-битных случайных чисел.
 * Использует два 64-битных числа для формирования одного 128-битного числа.
 * Реализует методы для генерации, вывода и анализа сгенерированных чисел.
 */
class RandomGenerator128 {
private:
    std::random_device rd;    ///< Устройство для получения случайных чисел
    std::mt19937_64 gen;      ///< Генератор случайных чисел Mersenne Twister
    uint64_t high_bits;       ///< Старшие 64 бита 128-битного числа
    uint64_t low_bits;        ///< Младшие 64 бита 128-битного числа

public:
    /**
     * @brief Конструктор генератора
     * 
     * Инициализирует генератор случайных чисел и генерирует первое число.
     */
    RandomGenerator128() : gen(rd()) {
        generate();
    }

    /**
     * @brief Генерирует новое 128-битное случайное число
     * 
     * Использует два вызова генератора для получения старших и младших 64 бит.
     */
    void generate() {
        high_bits = gen();
        low_bits = gen();
    }

    /**
     * @brief Возвращает текущее число в виде двоичной строки
     * 
     * Преобразует старшие и младшие 64 бита в строку из нулей и единиц.
     * 
     * @return std::string строка из 128 символов, представляющая число в двоичном виде
     */
    std::string get_binary_string() const {
        std::bitset<64> hi(high_bits), lo(low_bits);
        return hi.to_string() + lo.to_string();
    }

    /**
     * @brief Выводит текущее число в двоичном виде
     * 
     * Выводит 128-битное число в виде строки из нулей и единиц в консоль.
     */
    void print_binary() const {
        std::cout << get_binary_string() << std::endl;
    }

    /**
     * @brief Подсчитывает количество нулей и единиц
     * 
     * Анализирует текущее число и выводит количество нулей и единиц в консоль.
     */
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

/**
 * @brief Точка входа в программу
 * 
 * Демонстрирует работу генератора случайных чисел:
 * - Создает генератор
 * - Выводит сгенерированное число
 * - Подсчитывает количество нулей и единиц
 * 
 * @return int код завершения программы
 */
int main() {
    setlocale(LC_ALL, "ru_RU.UTF-8");

    RandomGenerator128 generator;
    std::cout << "Сгенерированное число в двоичном виде:" << std::endl;
    generator.print_binary();
    generator.count_bits();
    
    return 0;
}