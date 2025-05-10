export const changeDescription = async (newDescription: string) => {
    console.log('New description: ', newDescription);
    try {
        await fetch(`http://localhost:8000/users/me/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ user: { description: newDescription } }),
        });
    } catch (error) {
        console.error('updating description error error:', error);
        throw error;
    }
};
