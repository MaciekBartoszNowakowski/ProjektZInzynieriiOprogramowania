export const rejectSubmission = async (submissionId: number) => {
    const response = await fetch(
        `http://localhost:8000/applications/submissions/${submissionId}/reject/`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        },
    );

    if (!response.ok) {
        throw new Error(`Reject failed: ${response.status}`);
    }

    return await response.json();
};
