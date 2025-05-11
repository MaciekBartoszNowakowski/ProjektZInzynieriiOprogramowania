export const searchTheses = async ({
    tags = [],
    department,
    thesis_type = [],
    language,
    limit = 10,
    offset = 0,
}: {
    tags?: string[];
    department?: string;
    thesis_type?: string[];
    language?: string;
    limit?: number;
    offset?: number;
}) => {
    try {
        const query = new URLSearchParams();

        tags.forEach((tag) => query.append('tags', tag));
        thesis_type.forEach((type) => query.append('thesis_type', type));
        if (department) query.append('department', department);
        if (language) query.append('language', language);
        query.append('limit', limit.toString());
        query.append('offset', offset.toString());

        const response = await fetch(
            `http://localhost:8000/common/search-topics/?${query.toString()}`,
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
        return data;
    } catch (error) {
        console.error('Downloading filtered theses error:', error);
        throw error;
    }
};
