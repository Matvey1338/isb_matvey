from flask import Flask, render_template, request, redirect, url_for
from collections import Counter

app = Flask(__name__)

# Пример зашифрованного текста.
# Здесь должен быть ваш зашифрованный текст из второй части задания.
encrypted_text = ("ПРИМЕР ЗАШИФРОВАННОГО ТЕКСТА, "
                  "КОТОРЫЙ ЗАМЕНЕН ЗА ГОСТЕВОЙ СИСТЕМОЙ И ПРОДЕМОНСТРИРОВАН "
                  "ДЛЯ ДЕМОНСТРАЦИИ РАБОТЫ ПРИЛОЖЕНИЯ.")


def get_frequency(text):
    """
    Возвращает список символов с их нормализованной частотой появления.
    Формат:
    [('А', 0.034), ('Б', 0.005), ..., (' ', 0.128)]
    """
    allowed_chars = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
    filtered_text = [ch for ch in text if ch in allowed_chars]
    total = len(filtered_text)

    # Подсчёт частот
    counter = Counter(filtered_text)

    # Гарантируем, что все буквы будут присутствовать, даже если 0
    for ch in allowed_chars:
        counter.setdefault(ch, 0)

    # Нормализация
    freq_list = sorted(
        [(ch, round(counter[ch] / total, 6)) for ch in allowed_chars],
        key = lambda x: x[1],
        reverse = True
    )

    return freq_list

def substitute_text(text, mapping):
    """
    Функция для замены символов.
    mapping — словарь вида { 'Оригинал': 'Замена', ... }
    """
    result = ""
    for ch in text:
        # Если символ есть в карте замены, то заменяем
        result += mapping.get(ch, ch)
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Главная страница: вывод зашифрованного текста и его частотный анализ.
    """
    freq = get_frequency(encrypted_text)
    return render_template("index.html",
                           encrypted_text=encrypted_text,
                           frequency=freq)

@app.route("/substitution", methods=["GET", "POST"])
def substitution():
    """
    Страница для замены букв: пользователь вводит букву и её замену.
    Допускается множественная замена (по одному правилу за раз).
    """
    result_text = encrypted_text
    mapping = {}
    if request.method == "POST":
        # Получаем список замен (можно добавить несколько пар)
        # Например, в форме два поля: letter_from и letter_to.
        letter_from = request.form.get("letter_from", "").strip().upper()
        letter_to = request.form.get("letter_to", "").strip().upper()
        if letter_from and letter_to:
            mapping[letter_from] = letter_to
        # Можно расширить логику для добавления нескольких правил.
        result_text = substitute_text(encrypted_text, mapping)
    return render_template("substitution.html",
                           original_text=encrypted_text,
                           result_text=result_text)


if __name__ == "__main__":
    app.run(debug=True)
