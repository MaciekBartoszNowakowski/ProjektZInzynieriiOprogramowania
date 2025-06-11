export const acceptSubmission = async (submissionId: number) => {
    const response = await fetch(
        `http://localhost:8000/applications/submissions/${submissionId}/accept/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        },
    );

    if (!response.ok) {
        throw new Error(`Accept failed: ${response.status}`);
    }

    return await response.json();
};
