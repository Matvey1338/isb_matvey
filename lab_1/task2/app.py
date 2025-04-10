from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)


def get_frequency(text):
    """
    Возвращает частоту всех видимых символов текста (оставляя пробел).
    """
    # Убираем переводы строк, табы и т.п., но оставляем пробел
    cleaned_text = text.replace('\n', '').replace('\r', '').replace('\t', '')

    total = len(cleaned_text)
    counter = Counter(cleaned_text)

    freq_list = sorted(
        [(ch, round(count / total, 6)) for ch, count in counter.items()],
        key=lambda x: x[1],
        reverse=True
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
    text_input = ""
    frequency = []
    if request.method == "POST":
        text_input = request.form.get("ciphertext", "")
        frequency = get_frequency(text_input)
    return render_template("index.html", input_text=text_input, frequency=frequency)


@app.route("/substitution", methods=["GET", "POST"])
def substitution():
    """
    Страница для замены букв: пользователь вводит текст и пары замен.
    """
    input_text = ""
    result_text = ""
    mapping = {}

    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        letter_from = request.form.get("letter_from", "")
        letter_to = request.form.get("letter_to", "")

        if input_text and letter_from and letter_to:
            mapping[letter_from] = letter_to
            result_text = substitute_text(input_text, mapping)
        else:
            result_text = input_text  # ничего не меняем

    return render_template("substitution.html",
                           original_text=input_text,
                           result_text=result_text)


if __name__ == "__main__":
    app.run(debug=True)
