export const updateTags = async (addedTags: string[], removedTags: string[]) => {
    try {
        await fetch(`http://localhost:8000/users/me/tags/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ to_add: addedTags, to_remove: removedTags }),
        });
    } catch (error) {
        console.error('updating tags error:', error);
        throw error;
    }
};
