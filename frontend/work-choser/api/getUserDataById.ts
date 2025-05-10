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
        return data;
    } catch (error) {
        console.error('downloading user data error:', error);
        throw error;
    }
};
