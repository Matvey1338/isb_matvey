class VigenereCipher:
    def __init__(self, key):
        """
        Инициализирует шифр Виженера с заданным ключом и алфавитом

        :param key: Ключ шифрования
        """
        self.key = key.lower()
        self.alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def encrypt(self, text):
        """
        Шифрует текст с использованием шифра Виженера

        :param text: Текст для шифрования
        :return: Зашифрованный текст
        """
        result = []
        key_index = 0

        for char in text:
            char_lower = char.lower()
            if char_lower in self.alphabet:
                # Вычисляем сдвиг на основе символа ключа
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.find(key_char)

                # Находим позицию символа в алфавите
                char_index = self.alphabet.find(char_lower)

                encrypted_index = (char_index + key_shift) % len(self.alphabet)
                encrypted_char = self.alphabet[encrypted_index]

                # Сохраняем регистр
                if char.isupper():
                    encrypted_char = encrypted_char.upper()

                result.append(encrypted_char)
                key_index += 1
            else:
                # Если символа нет в алфавите, оставляем как есть
                result.append(char)

        return ''.join(result)

    def decrypt(self, text):
        """
        Дешифрует текст, зашифрованный шифром Виженера

        :param text: Зашифрованный текст
        :return: Дешифрованный текст
        """
        result = []
        key_index = 0

        for char in text:
            char_lower = char.lower()
            if char_lower in self.alphabet:
                # Вычисляем сдвиг на основе символа ключа
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.find(key_char)

                # Находим позицию символа в алфавите
                char_index = self.alphabet.find(char_lower)

                decrypted_index = (char_index - key_shift) % len(self.alphabet)
                decrypted_char = self.alphabet[decrypted_index]

                # Сохраняем регистр
                if char.isupper():
                    decrypted_char = decrypted_char.upper()

                result.append(decrypted_char)
                key_index += 1
            else:
                # Если символа нет в алфавите, оставляем как есть
                result.append(char)

        return ''.join(result)

    def get_key(self):
        """
        Возвращает ключ шифрования

        :return: Ключ шифрования
        """
        return self.key
