import os
import json
import re


def save_key(key, filename='encryption_key.json'):
    """
    Сохраняет ключ шифрования в JSON-файл

    :param key: Ключ шифрования
    :param filename: Имя файла
    :return: Полный путь к файлу
    """
    os.makedirs(os.path.dirname(filename), exist_ok = True)

    key_data = {
        'key': key,
    }

    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(key_data, file, ensure_ascii = False, indent = 4)

    return os.path.abspath(filename)


def get_next_index(output_dir):
    files = os.listdir(output_dir)
    pattern = re.compile(r'key_(\d+)\.json')
    indices = [
        int(match.group(1))
        for file in files
        if (match := pattern.match(file))
    ]
    return max(indices, default=0) + 1


def save_file(output_dir, text):
    with open(output_dir, 'w', encoding='utf-8') as f:
        f.write(text)