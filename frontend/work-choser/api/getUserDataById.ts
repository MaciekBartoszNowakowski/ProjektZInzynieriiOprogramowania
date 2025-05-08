export const getUserDataById = async (id: string) => {
    try {
        const response = await fetch(`http://localhost:8000/users/${id}`, {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data; // możesz też return data.user;
    } catch (error) {
        console.error('Błąd przy pobieraniu użytkownika:', error);
        throw error;
    }
};
