export const getThesisSubmissions = async (thesisId: number) => {
    try {
        const response = await fetch(
            `http://localhost:8000/applications/thesis/${thesisId}/submissions/`,
            {
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            },
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        return data.submissions;
    } catch (error) {
        console.error('Error fetching submissions:', error);
        throw error;
    }
};
