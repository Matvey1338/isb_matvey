document.addEventListener('DOMContentLoaded', function() {
    // Переключение вкладок
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем активный класс со всех кнопок и скрываем все вкладки
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.add('hidden'));

            // Добавляем активный класс нажатой кнопке и показываем соответствующую вкладку
            this.classList.add('active');
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-tab`).classList.remove('hidden');
        });
    });

    // Загрузка файлов
    const fileInputs = document.querySelectorAll('.file-input');

    fileInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Ошибка: ' + data.error);
                    return;
                }

                // Получаем ID соответствующего текстового поля
                const textareaId = this.id.replace('file', 'text');
                document.getElementById(textareaId).value = data.text;
            })
            .catch(error => {
                console.error('Ошибка загрузки файла:', error);
                alert('Произошла ошибка при загрузке файла');
            });
        });
    });
});