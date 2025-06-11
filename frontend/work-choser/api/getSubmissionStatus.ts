export const getSubmissionStatus = async () => {
    try {
        const response = await fetch('http://localhost:8000/applications/status/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, data };
        } else {
            console.error('serwer error:', data);
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('network error:', error);
        return { success: false, error };
    }
};
