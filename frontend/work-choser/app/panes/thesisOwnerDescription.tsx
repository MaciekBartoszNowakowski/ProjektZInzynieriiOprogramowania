import { useRoute, RouteProp } from '@react-navigation/native';
import { useEffect, useState } from 'react';
import { View, Text, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisById } from '@/api/getThesisById';
import { StackParamList } from '@/types/navigationTypes';
import PendingStudentList from '@/components/custom_components/pendingStudentList';

export default function ThesisOwnerDescription() {
    const route = useRoute<RouteProp<StackParamList, 'ThesisOwnerDescription'>>();
    const { thesisId } = route.params;

    const [thesis, setThesis] = useState<any>(null);

    useEffect(() => {
        const fetchThesis = async () => {
            try {
                console.log('Fetching thesis with ID:', thesisId);
                const data = await getThesisById(thesisId);
                console.log('Fetched thesis:', data);
                setThesis(data);
            } catch (error) {
                console.error('Failed to fetch thesis:', error);
            }
        };

        fetchThesis();
    }, [thesisId]);

    if (!thesis) {
        return (
            <View style={styles.container}>
                <Text style={styles.textBox}>Loading thesis data...</Text>
            </View>
        );
    }

    const supervisor = thesis.supervisor_id.user;
    const fullName = `${supervisor.academic_title} ${supervisor.first_name} ${supervisor.last_name}`;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Thesis Title</Text>
                <Text style={styles.textBox}>{thesis.name}</Text>

                <Text style={styles.titleTextBox}>Supervisor</Text>
                <Text style={styles.textBox}>{fullName}</Text>

                <Text style={styles.titleTextBox}>Availability</Text>
                <Text style={styles.textBox}>
                    Free slots: <Text style={styles.slotValue}>x</Text> Busy slots:{' '}
                    <Text style={styles.slotValue}>y</Text> Pending slots:{' '}
                    <Text style={styles.slotValue}>z</Text>
                </Text>
            </View>

            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Thesis Description</Text>
                <Text style={styles.textBox}>{thesis.description}</Text>
            </View>
            <PendingStudentList />
        </ScrollView>
    );
}
