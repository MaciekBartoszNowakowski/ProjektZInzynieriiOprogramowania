import { View, Text, FlatList, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisSubmissions } from '@/api/getThesisSubmissions';
import { useEffect, useState } from 'react';
import { Submission } from '@/types/submissionType';
import { acceptSubmission } from '@/api/acceptSubmission';
import { rejectSubmission } from '@/api/rejectSubmission';
export default function PendingStudentList({ thesisId }: { thesisId: number }) {
    const [submissions, setSubmissions] = useState<Submission[]>([]);

    useEffect(() => {
        getThesisSubmissions(thesisId)
            .then(setSubmissions)
            .catch((err) => console.error('Error fetching submissions:', err));
    }, [thesisId]);

    return (
        <View style={styles.mainStudentListBox}>
            <Text style={styles.titleStudentListText}>Zgłoszeni studenci</Text>

            <FlatList
                data={submissions}
                keyExtractor={(item) => item.student.index_number}
                renderItem={({ item }) => (
                    <View style={styles.singleElementFormStudentList}>
                        <Text style={styles.textBox}>{item.student.full_name}</Text>

                        <View style={styles.flexViewStyle}>
                            <TouchableOpacity
                                style={styles.signInButton}
                                onPress={async () => {
                                    try {
                                        await acceptSubmission(item.id);
                                        console.log(`Accepted: ${item.student.full_name}`);
                                        setSubmissions((prev) =>
                                            prev.filter((s) => s.id !== item.id),
                                        );
                                    } catch (e) {
                                        console.error('Accept error:', e);
                                    }
                                }}
                            >
                                <Text style={styles.buttonText}>Zaakceptuj</Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={styles.declineButton}
                                onPress={async () => {
                                    try {
                                        await rejectSubmission(item.id);
                                        console.log(`Rejected: ${item.student.full_name}`);
                                        setSubmissions((prev) =>
                                            prev.filter((s) => s.id !== item.id),
                                        );
                                    } catch (e) {
                                        console.error('Reject error:', e);
                                    }
                                }}
                            >
                                <Text style={styles.buttonText}>Odrzuć</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                )}
            />
        </View>
    );
}
