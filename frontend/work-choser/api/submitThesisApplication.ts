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

        if (!response.ok) {
            const errorText = await response.text();
            return { success: false, error: errorText };
        }

        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        return { success: false, error: error instanceof Error ? error.message : String(error) };
    }
};
