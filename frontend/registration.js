let usernameInput = document.getElementById('Username');
let passwordInput = document.getElementById('Password');
let mailInput = document.getElementById('Mail');
let registerBtn = document.getElementById('Register'); // Кнопка в HTML

// Функция для сохранения токенов и перехода на главную страницу
function saveTokensAndRedirect(data, username) {
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('username', username); // Чтобы подставить имя в шапку сайта
    window.location.href = "sait.html";
}

registerBtn.addEventListener("click", async function(event) {
    event.preventDefault(); // Отменяем перезагрузку страницы

    let username = usernameInput.value.trim();
    let password = passwordInput.value.trim();
    let email = mailInput.value.trim();

    // 1. Проверяем, чтобы поля не пустовали
    if (username === "" || password === "" || email === "") {
        alert("Заполни все поля!");
        return;
    }

    try {
        // 2. ИСХОД: Пробуем зарегистрировать нового пользователя
        console.log("Отправляем запрос на регистрацию...");
        
        let registerResponse = await fetch('http://localhost:8000/auth/register', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password,
                email: email
            })
        });

        // Если пользователя не было в базе — регистрация успешна
        if (registerResponse.ok) {
            let data = await registerResponse.json();
            alert("Добро пожаловать! Аккаунт успешно создан.");
            saveTokensAndRedirect(data, username);
            return; 
        }

        // Читаем текст ошибки от сервера, чтобы понять причину
        let errorData = await registerResponse.json();

        // 3. ИСХОД: Если сервер ответил "User already exists" (юзер уже есть)
        if (registerResponse.status === 400 || errorData.detail === "User already exists") {
            console.log("Юзер уже есть в БД. Молча переключаемся на авторизацию...");

            let loginResponse = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            // Если пароль правильный — успешно входим
            if (loginResponse.ok) {
                let data = await loginResponse.json();
                alert("Рады видеть снова! Вход выполнен.");
                saveTokensAndRedirect(data, username);
            } else {
                // Если юзер существует, но пароль к нему ввели неправильный
                let loginError = await loginResponse.json();
                alert("Ошибка: " + (loginError.detail || "Неверный пароль для этого пользователя."));
            }
        } else {
            // Если случилась какая-то другая ошибка регистрации (например, пароль слишком короткий)
            alert("Ошибка регистрации: " + (errorData.detail || "Неверные данные"));
        }

    } catch (error) {
        console.error("Критическая ошибка сети:", error);
        alert("Не удалось связаться с сервером. Убедись, что Docker запущен!");
    }
});Ф