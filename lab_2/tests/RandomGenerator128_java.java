import java.util.Random;

/**
 * Генератор случайных 128-битных чисел.
 * Использует два 64-битных числа для формирования одного 128-битного числа.
 * Предоставляет методы для генерации, вывода и анализа сгенерированных чисел.
 */
public class RandomGenerator128_java {
    /** Генератор случайных чисел */
    private Random random;
    /** Старшие 64 бита 128-битного числа */
    private long highBits;
    /** Младшие 64 бита 128-битного числа */
    private long lowBits;

    /**
     * Создает новый генератор случайных чисел и генерирует первое число.
     */
    public RandomGenerator128_java() {
        random = new Random();
        generate();
    }

    /**
     * Генерирует новое 128-битное случайное число.
     * Использует два вызова nextLong() для получения старших и младших 64 бит.
     */
    public void generate() {
        highBits = random.nextLong();
        lowBits = random.nextLong();
    }

    /**
     * Возвращает 128-битное число в виде строки из нулей и единиц.
     * Дополняет каждую 64-битную часть нулями слева до 64 символов.
     *
     * @return строка из 128 символов, представляющая число в двоичном виде
     */
    public String getBinaryString() {
        String highStr = String.format("%64s", Long.toBinaryString(highBits)).replace(' ', '0');
        String lowStr = String.format("%64s", Long.toBinaryString(lowBits)).replace(' ', '0');
        return highStr + lowStr;
    }

    /**
     * Выводит текущее 128-битное число в двоичном виде в консоль.
     */
    public void printBinary() {
        System.out.println(getBinaryString());
    }

    /**
     * Подсчитывает количество нулей и единиц в текущем числе
     * и выводит результат в консоль.
     */
    public void countBits() {
        String binary = getBinaryString();
        int zeros = 0;
        int ones = 0;
        
        for (char bit : binary.toCharArray()) {
            if (bit == '0') zeros++;
            else ones++;
        }
        
        System.out.println("Number of zeros: " + zeros);
        System.out.println("Number of ones: " + ones);
    }

    public static void main(String[] args) {
        RandomGenerator128_java generator = new RandomGenerator128_java();
        System.out.println("Generated number in binary:");
        generator.printBinary();
        generator.countBits();
    }
} 