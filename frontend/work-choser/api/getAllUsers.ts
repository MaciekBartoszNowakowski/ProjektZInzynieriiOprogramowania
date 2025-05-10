interface User {
    url: string;
    academic_title: string;
    first_name: string;
    last_name: string;
    email: string;
    role: string;
    department_name?: string;
    tags?: string[];
}

export const getAllUsers = async (params: Record<string, any> = {}): Promise<User[]> => {
    try {
        let query = '';
        const queryParts: string[] = [];

        Object.entries(params).forEach(([key, value]) => {
            if (Array.isArray(value)) {
                value.forEach((v) =>
                    queryParts.push(`${encodeURIComponent(key)}=${encodeURIComponent(v)}`),
                );
            } else {
                queryParts.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
            }
        });

        if (queryParts.length > 0) {
            query = '?' + queryParts.join('&');
        }

        const response = await fetch(`http://localhost:8000/common/search-users/${query}`, {
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
        console.error('downloading users error:', error);
        throw error;
    }
};
