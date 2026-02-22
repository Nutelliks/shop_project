class AuthAPI {
    constructor() {
        this.baseURL = '/user/api/auth';  // базовый URL всех эндпоинтов
        this.accessToken = localStorage.getItem('accessToken');
        this.refreshToken = localStorage.getItem('refreshToken');
    }

    // Сохраняем токены в localStorage и в свойства класса
    setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    }

    // Удаляем токены (при выходе или ошибке)
    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    // Проверка, авторизован ли пользователь
    isAuthenticated() {
        return !!this.accessToken;
    }

    // Базовый метод для запросов с автоматическим добавлением заголовка Authorization
    async request(endpoint, options = {}) {
        const url = this.baseURL + endpoint;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        const config = {
            ...options,
            headers,
            credentials: 'same-origin'  // для передачи cookies, если понадобятся
        };

        let response = await fetch(url, config);

        // Если получили 401 и у нас есть refresh токен — пробуем обновить access
        if (response.status === 401 && this.refreshToken) {
            const refreshed = await this.refreshAccessToken();
            if (refreshed) {
                // Повторяем исходный запрос с новым токеном
                headers['Authorization'] = `Bearer ${this.accessToken}`;
                response = await fetch(url, config);
            }
        }

        return response;
    }

    // Метод для обновления access токена
    async refreshAccessToken() {
        try {
            const response = await fetch(`${this.baseURL}/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: this.refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                // Обновляем только access token, refresh остаётся тем же
                this.setTokens(data.access, this.refreshToken);
                return true;
            } else {
                // Если refresh токен протух или недействителен — разлогиниваем
                this.clearTokens();
                return false;
            }
        } catch (error) {
            console.error('Refresh token error:', error);
            this.clearTokens();
            return false;
        }
    }

     // Регистрация
    async register(userData) {
        const response = await fetch(`${this.baseURL}/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return response;
    }

    // Вход в систему
    async login(credentials) {
        const response = await fetch(`${this.baseURL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        });

        try {
            const data = await response.json();
            if (response.ok) {
                this.setTokens(data.access, data.refresh);
            }
            // Сохраняем данные для использования в других частях кода
            response.data = data;
        } catch (e) {
            response.data = {};
        }
        return response;
    }
}

const api = new AuthAPI();