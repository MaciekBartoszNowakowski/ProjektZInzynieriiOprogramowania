export const submitThesisApplication = async (thesisId: number) => {
    try {
        const response = await fetch('http://localhost:8000/applications/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ thesis_id: thesisId }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('success ', data);
            return { success: true, data };
        } else {
            console.error('serwer error', data);
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Błąd sieci:', error);
        return { success: false, error };
    }
};
