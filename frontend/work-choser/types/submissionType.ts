export type Submission = {
    id: number;
    student: {
        index_number: string;
        full_name: string;
    };
    thesis: {
        id: number;
        name: string;
        thesis_type: string;
        description: string;
        status: string;
        language: string;
        supervisor_name: string;
    };
    status: string;
};
