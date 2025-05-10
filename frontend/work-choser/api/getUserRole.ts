export const getUserRole = async () => {
    try {
        const response = await fetch('http://localhost:8000/users/me/', {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        const data = await response.json();

        if (response.ok && data.user && data.user.role && data.user?.id) {
            return { role: data.user.role, id: data.user.id };
        } else {
            console.error('empty role: ', data);
        }
    } catch (error) {
        console.error('Web error: ', error);
    }
};
