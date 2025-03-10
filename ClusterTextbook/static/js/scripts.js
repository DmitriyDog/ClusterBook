// Функция для отметки статьи как прочитанной
function markAsRead() {
    // Получаем элемент статьи
    const article = document.getElementById('article');

    // Если статья еще не отмечена как прочитанная
    if (!article.classList.contains('read')) {
        // Добавляем класс read
        article.classList.add('read');

        // Сохраняем идентификатор статьи в localStorage
        localStorage.setItem('readArticles', JSON.stringify([...new Set(JSON.parse(localStorage.getItem('readArticles') || '[]'), article.id)]));
    }
}

// Функция для проверки статуса статьи при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
    const article = document.getElementById('article');

    // Проверяем, была ли статья отмечена как прочитанная ранее
    const readArticles = JSON.parse(localStorage.getItem('readArticles') || '[]');

    if (readArticles.includes(article.id)) {
        // Если да, добавляем класс read
        article.classList.add('read');
    }
});