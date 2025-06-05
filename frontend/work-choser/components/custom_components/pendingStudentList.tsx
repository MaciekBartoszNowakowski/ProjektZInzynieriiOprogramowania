import { View, Text, FlatList, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisSubmissions } from '@/api/getThesisSubmissions';
import { useEffect, useState } from 'react';
import { Submission } from '@/types/submissionType';
import { acceptSubmission } from '@/api/acceptSubmission';
import { rejectSubmission } from '@/api/rejectSubmission';
import { getThesisById } from '@/api/getThesisById';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { StackParamList } from '@/types/navigationTypes';

// type StackParamList = {
//     StudentProfile: { id: number };
// };

export default function PendingStudentList({ thesisId }: { thesisId: number }) {
    const [submissions, setSubmissions] = useState<Submission[]>([]);
    const [maxStudents, setMaxStudents] = useState<number>(Infinity);
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();

    useEffect(() => {
        const fetchAll = async () => {
            try {
                const [submissionData, thesisData] = await Promise.all([
                    getThesisSubmissions(thesisId),
                    getThesisById(thesisId),
                ]);
                setSubmissions(submissionData);
                setMaxStudents(thesisData.max_students);
            } catch (err) {
                console.error('Error fetching data:', err);
            }
        };
        fetchAll();
    }, [thesisId]);

    const handleAccept = async (id: number) => {
        try {
            await acceptSubmission(id);
            const updated = submissions.map((s) =>
                s.id === id ? { ...s, status: 'zaakceptowane' } : s,
            );
            console.log(
                'Aktualne statusy:',
                updated.map((s) => ({ id: s.id, status: s.status })),
            );

            setSubmissions(updated);

            const acceptedCount = updated.filter((s) => s.status === 'zaakceptowane').length;
            if (acceptedCount >= maxStudents) {
                const toReject = updated.filter((s) => s.status === 'aktywne');
                await Promise.all(toReject.map((s) => rejectSubmission(s.id)));
                setSubmissions((prev) =>
                    prev.map((s) =>
                        s.status === 'oczekujące' ? { ...s, status: 'odrzucone' } : s,
                    ),
                );
            }
        } catch (e) {
            console.error('Accept error:', e);
        }
    };

    const handleReject = async (id: number) => {
        try {
            console.log('Odrzucam:', id);

            await rejectSubmission(id);
            setSubmissions((prev) =>
                prev.map((s) => (s.id === id ? { ...s, status: 'odrzucone' } : s)),
            );
        } catch (e) {
            console.error('Reject error:', e);
        }
    };
    return (
        <View style={styles.mainStudentListBox}>
            <Text style={styles.titleStudentListText}>Zgłoszeni studenci</Text>

            <FlatList
                data={submissions}
                keyExtractor={(item) => item.student.index_number}
                renderItem={({ item }) => (
                    <View style={styles.singleElementFormStudentList}>
                        {/* <Text style={styles.textBox}>{item.student.full_name}</Text>
                        <Text style={styles.textBox}>Status: {item.status}</Text> */}
                        <TouchableOpacity
                            onPress={() =>
                                navigation.navigate('StudentProfile', {
                                    id: Number(item.student),
                                })
                            }
                        >
                            <Text style={styles.textBox}>{item.student.full_name}</Text>
                        </TouchableOpacity>
                        <Text style={styles.textBox}>Status: {item.status}</Text>
                        <View style={styles.flexViewStyle}>
                            <TouchableOpacity
                                style={styles.signInButton}
                                onPress={() => handleAccept(item.id)}
                                disabled={item.status !== 'aktywne'}
                            >
                                <Text style={styles.buttonText}>Zaakceptuj</Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={styles.declineButton}
                                onPress={() => handleReject(item.id)}
                                disabled={item.status !== 'aktywne'}
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
