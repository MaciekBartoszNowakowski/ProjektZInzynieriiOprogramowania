import { useRoute, RouteProp } from '@react-navigation/native';
import { useEffect, useState } from 'react';
import { View, Text, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisById } from '@/api/getThesisById';
import { getThesisSubmissions } from '@/api/getThesisSubmissions';
import { StackParamList } from '@/types/navigationTypes';
import PendingStudentList from '@/components/custom_components/pendingStudentList';

export default function ThesisOwnerDescription() {
    const route = useRoute<RouteProp<StackParamList, 'ThesisOwnerDescription'>>();
    const { thesisId } = route.params;

    const [thesis, setThesis] = useState<any>(null);
    const [submissions, setSubmissions] = useState<any[]>([]);

    const refreshData = async () => {
        try {
            const thesisData = await getThesisById(thesisId);
            setThesis(thesisData);

            const submissionData = await getThesisSubmissions(thesisId);
            setSubmissions(submissionData);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    };

    useEffect(() => {
        refreshData();
    }, [thesisId]);

    if (!thesis) {
        return (
            <View style={styles.container}>
                <Text style={styles.textBox}>Pobieranie danych...</Text>
            </View>
        );
    }

    const supervisor = thesis.supervisor_id.user;
    const fullName = `${supervisor.academic_title} ${supervisor.first_name} ${supervisor.last_name}`;
    const acceptedCount = submissions.filter((s) => s.status === 'zaakceptowane').length;
    const pendingCount = submissions.filter((s) => s.status === 'aktywne').length;
    const availableCount = thesis.max_students - acceptedCount;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Tytuł pracy</Text>
                <Text style={styles.textBox}>{thesis.name}</Text>

                <Text style={styles.titleTextBox}>Promotor</Text>
                <Text style={styles.textBox}>{fullName}</Text>

                <Text style={styles.titleTextBox}>Dostępność</Text>
                <Text style={styles.textBox}>
                    Dostępne miejsca: <Text style={styles.slotValue}>{availableCount} </Text>
                    Zajęte miejsca: <Text style={styles.slotValue}>{acceptedCount} </Text>
                    Oczekujące zgłoszenia: <Text style={styles.slotValue}>{pendingCount}</Text>
                </Text>
            </View>

            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Opis pracy</Text>
                <Text style={styles.textBox}>{thesis.description}</Text>
            </View>
            <PendingStudentList thesisId={thesisId} />
        </ScrollView>
    );
}
