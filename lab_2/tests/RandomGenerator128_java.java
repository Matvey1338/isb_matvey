import java.util.Random;

public class RandomGenerator128_java {
    private Random random;
    private long highBits;
    private long lowBits;

    public RandomGenerator128_java() {
        random = new Random();
        generate();
    }

    public void generate() {
        highBits = random.nextLong();
        lowBits = random.nextLong();
    }

    public String getBinaryString() {
        String highStr = String.format("%64s", Long.toBinaryString(highBits)).replace(' ', '0');
        String lowStr = String.format("%64s", Long.toBinaryString(lowBits)).replace(' ', '0');
        return highStr + lowStr;
    }

    public void printBinary() {
        System.out.println(getBinaryString());
    }

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