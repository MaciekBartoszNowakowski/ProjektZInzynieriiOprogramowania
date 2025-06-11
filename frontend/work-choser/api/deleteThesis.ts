export const deleteThesis = async (id: number) => {
    try {
        const response = await fetch(`http://localhost:8000/thesis/delete/${id}`, {
            method: 'DELETE',
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error(`Błąd usuwania pracy. Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Błąd podczas usuwania pracy:', error);
        throw error;
    }
};
