export const getAllTheses = async () => {
    try {
        const response = await fetch(`http://localhost:8000/thesis/available`, {
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
        console.error('donloading tags error:', error);
        throw error;
    }
};
