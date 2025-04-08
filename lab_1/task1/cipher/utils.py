import os
import json
from datetime import datetime


def save_key(key, key_info=None, filename='encryption_key.json'):
    """
    Сохраняет ключ шифрования в JSON-файл

    :param key: Ключ шифрования
    :param key_info: Дополнительная информация о ключе
    :param filename: Имя файла
    :return: Полный путь к файлу
    """
    os.makedirs(os.path.dirname(filename), exist_ok = True)

    key_data = {
        'key': key,
    }

    if key_info:
        key_data.update(key_info)

    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(key_data, file, ensure_ascii = False, indent = 4)

    return os.path.abspath(filename)
