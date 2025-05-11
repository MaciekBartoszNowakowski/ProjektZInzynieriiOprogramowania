export const sendLoginData = async (login: string, password: string) => {
    try {
        const response = await fetch('http://localhost:8000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ username: login, password: password }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Sukces: ', data);
            return false;
        } else {
            console.error('serwer error: ', data);
            return true;
        }
    } catch (error) {
        console.error('Błąd sieci: ', error);
    }
};
