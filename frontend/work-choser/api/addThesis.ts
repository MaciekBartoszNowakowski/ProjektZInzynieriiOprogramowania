export const addThesis = async (data: {
    name: string;
    description?: string;
    max_students?: number;
    language?: string;
    thesis_type: string;
    tags: string[];
}) => {
    try {
        const response = await fetch('http://localhost:8000/thesis/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorText = await response.text();
            return { success: false, error: errorText };
        }

        const result = await response.json();
        return { success: true, data: result };
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
};
