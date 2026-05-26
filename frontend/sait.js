// 1. Словарь сопоставления строковых ID схемы с ID групп мышц на бэкенде
const people = {
    "trapecia": 1,
    "spina": 3,
    "perDel": 4,
    "serDel": 5,
    "zadDel": 6,
    "biceps": 7,
    "tricips": 8,
    "predpleche": 9, 
    "siski": 10, 
    "pres": 11,
    "cos": 12,
   "kvadri": 13,
    "zadPowerx": 14,
    "ikri": 15,
    "popa": 16,
};

// Глобальная переменная для левого сайдбара
let leftSidebar = null;

document.addEventListener("DOMContentLoaded", function () {

    // Поиск элементов интерфейса
    const userLink = document.querySelector('.user-info a');
    const userText = userLink ? userLink.querySelector('p') : null;
    leftSidebar = document.querySelector('.left-sidebar');
    const rightSidebar = document.querySelector('.right-sidebar');

    // Базовый URL бэкенда
    const BACKEND_URL = 'http://localhost:8000';

    // Функция для выполнения запросов с авторизацией
    async function fetchWithAuth(url, options = {}) {
        let accessToken = localStorage.getItem('access_token');

        if (accessToken) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            };
        }

        let response = await fetch(url, options);

        // Если токен просрочен (401), пытаемся его обновить автоматически без ведома пользователя
        if (response.status === 401) {
            console.log("Access-токен просрочен. Запуск автоматического обновления...");

            const isRefreshed = await refreshTokens();

            if (isRefreshed) {
                // Если обновили успешно — берем новый токен и повторяем запрос
                accessToken = localStorage.getItem('access_token');
                options.headers['Authorization'] = `Bearer ${accessToken}`;
                response = await fetch(url, options);
            } else {
                console.log("Авто-рефреш не удался. Требуется ручной вход.");
                alert("Время сессии истекло. Пожалуйста, авторизуйтесь снова.");
                localStorage.clear();
                window.location.href = "registration.html";
                return null;
            }
        }

        return response;
    }

    // передает данные всеми доступными бэкенду способами
    async function refreshTokens() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) return false;

        try {
            // Отправляем и в заголовках (Bearer), и в теле (JSON) — так бэк поймет запрос 
            const response = await fetch(`${BACKEND_URL}/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${refreshToken}`
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();

                // Перезаписываем токены
                localStorage.setItem('access_token', data.access_token);
                if (data.refresh_token) {
                    localStorage.setItem('refresh_token', data.refresh_token);
                }
                console.log("Токены автоматически обновлены в фоне!");
                return true;
            } else {
                console.error(`Бэкенд отказался обновлять токен. Статус: ${response.status}`);
            }
        } catch (error) {
            console.error("Критическая ошибка при попытке рефреша токенов:", error);
        }
        return false;
    }

    // Инициализация контента правого сайдбара (Фитнес-советы)
    if (rightSidebar) {
        rightSidebar.innerHTML = `
            <h3>🥗 Фитнес-советы</h3>
            <ul>
                <li><strong>Правильное питание:</strong> <p class="info-mischci">Соблюдайте баланс БЖУ и пейте воду.</p></li>
                <li><strong>Режим отдыха:</strong> <p class="info-mischci">Мышцы растут во время сна (не менее 7-8 часов).</p></li>
                <li><strong>Безопасность:</strong> <p class="info-mischci">Всегда делайте суставную разминку перед тренировкой.</p></li>
            </ul>
        `;
    }

    // Функция проверки авторизации и настройки шапки сайта
    function checkAuth() {
        const refreshToken = localStorage.getItem('refresh_token');
        const savedUsername = localStorage.getItem('username');

        if (!refreshToken) {
            if (userText) userText.textContent = "Войти в аккаунт";
            if (userLink) {
                userLink.href = "registration.html";
                userLink.style.pointerEvents = "auto";
            }
            if (leftSidebar) {
                leftSidebar.innerHTML = `
                    <h3>Упражнение на твою группу мышц 🦾</h3>
                    <p class="info-mischci" style="color: #ff4d00; font-weight: bold; padding: 10px;">
                        ⚠️ Человечек доступен только после регистрации! Войдите в аккаунт.
                    </p>
                `;
            }
            return false;
        }

        if (savedUsername && userText && userLink) {
            userText.textContent = `${savedUsername} (Выйти)`;
            userLink.href = "#";
            userLink.style.pointerEvents = "auto";

            userLink.onclick = function (e) {
                e.preventDefault();
                localStorage.clear();
                location.reload();
            };
            return true;
        }
        return false;
    }

    // Функция получения данных о мышце и упражнениях с бэкенда
    async function getRockElement(muscleId) {
        const numericId = people[muscleId];
        if (numericId === undefined) {
            console.error(`Ошибка: Мышца "${muscleId}" не найдена в объекте people.`);
            return;
        }

        try {
            const response = await fetchWithAuth(`${BACKEND_URL}/rock/${numericId}`);

            if (!response || !response.ok) {
                throw new Error(`Сервер вернул ошибку: ${response ? response.status : 'нет ответа'}`);
            }

            const data = await response.json();
            console.log('Успешно получили элемент от бэка:', data);

            if (leftSidebar) {
                // 1. Формируем HTML для упражнений
                const hasExercises = Array.isArray(data.exercises) && data.exercises.length > 0;
                const exercisesHtml = hasExercises
                    ? data.exercises.map(ex => `
                    <li>
                        <strong>${ex.name || 'Упражнение'}:</strong> 
                        <p class="info-mischci">${ex.description || 'Описание отсутствует.'}</p>
                    </li>
                  `).join('')
                    : `<p class="info-mischci" style="font-style: italic; opacity: 0.8;">
                    В данный момент для этой группы мышц нет доступных упражнений.
                   </p>`;

                // 2. Добавляем описание самой мышцы (если оно есть в ответе бэка)
                const muscleDescHtml = data.muscle_description
                    ? `<p class="muscle-brief-desc" style="margin-bottom: 15px; font-weight: 500;">
                    ${data.muscle_description}
                   </p><hr style="opacity: 0.2; margin-bottom: 15px;">`
                    : '';

                // 3. Финальный рендеринг в сайдбар
                leftSidebar.innerHTML = `
                <h3>💪 ${data.muscle_name || muscleId}</h3>
                ${muscleDescHtml}
                ${hasExercises ? `<ul>${exercisesHtml}</ul>` : exercisesHtml}
            `;
            }

        } catch (error) {
            console.error('Ошибка при получении данных с бэка:', error);

            if (leftSidebar) {
                leftSidebar.innerHTML = `
                <h3>⚠️ Ошибка загрузки</h3>
                <p style="padding: 10px; color: red;">Не удалось получить данные с сервера. Проверьте соединение с бэкендом.</p>
            `;
            }
        }
    }

    // Лоадер перед отправкой запроса
    window.showExercises = function (muscleId) {
        if (!leftSidebar) return;
        leftSidebar.innerHTML = `<h3>Загрузка...</h3>`;
        getRockElement(muscleId);
    };

    // Навешивание обработчиков клика
    const muscleElements = document.querySelectorAll('.mischci');

    muscleElements.forEach(muscle => {
        muscle.addEventListener('click', async function () {
            // 1. Проверяем базовое наличие токена регистрации в браузере
            if (!checkAuth()) {
                alert("Чтобы взаимодействовать со схемой, необходимо авторизоваться!");
                window.location.href = "registration.html";
                return;
            }

            const muscleId = this.id;
            console.log(`Кликнули по id: ${muscleId}`);

            // 2. Упреждающая проверка: если ацесс токена нет физически (например, удален), 
            // сразу запрашиваем новый без лишнего падения запроса
            if (!localStorage.getItem('access_token')) {
                console.log("Допремьерный рефреш: access_token отсутствует. Обновляем...");
                await refreshTokens();
            }

            // 3. Запускаем загрузку упражнений
            window.showExercises(muscleId);
        });
    });

    checkAuth();
});