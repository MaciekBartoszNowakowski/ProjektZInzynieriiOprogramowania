export type StackParamList = {
    SupervisorProfile: { id: string };
    ThesisDescription: { thesisId: number };
    ThesisOwnerDescription: { thesisId: number };
    StudentProfile: { id: number };
    applicatedThesisDescription: {
        thesisId: number;
        name: string;
        supervisor: string;
        status: string;
        description: string;
    };
    AddingThesis: undefined;
};
