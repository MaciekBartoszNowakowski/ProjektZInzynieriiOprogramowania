export const cancelApplication = async () => {
    try {
        const response = await fetch('http://localhost:8000/applications/cancel/', {
            method: 'DELETE',
            credentials: 'include',
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('cancelApplication error:', errorData);
            throw new Error(errorData.message || 'Nie udało się anulować zgłoszenia');
        }

        return await response.json();
    } catch (error) {
        console.error('cancelApplication fetch error:', error);
        throw error;
    }
};
