export const getMyTheses = async () => {
    try {
        const response = await fetch('http://localhost:8000/thesis/my-topics', {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Błąd pobierania prac promotora:', error);
        throw error;
    }
};
