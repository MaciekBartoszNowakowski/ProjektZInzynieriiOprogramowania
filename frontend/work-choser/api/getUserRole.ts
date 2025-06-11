export const getUserRole = async () => {
    try {
        const response = await fetch('http://localhost:8000/users/me/', {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });

        const data = await response.json();

        if (response.ok && data.user && data.user.role && data.user.id) {
            return {
                id: data.user.id,
                role: data.user.role,
                bachelor_limit: data.bacherol_limit ?? 0,
                engineering_limit: data.engineering_limit ?? 0,
                master_limit: data.master_limit ?? 0,
                phd_limit: data.phd_limit ?? 0,
            };
        } else {
            console.error('Brak danych użytkownika lub roli:', data);
            return null;
        }
    } catch (error) {
        console.error('Błąd podczas pobierania roli użytkownika:', error);
        throw error;
    }
};
