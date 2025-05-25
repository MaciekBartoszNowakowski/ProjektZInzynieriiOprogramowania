import { useRoute, RouteProp } from '@react-navigation/native';
import { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisById } from '@/api/getThesisById';
import { StackParamList } from '@/types/navigationTypes';

export default function ThesisDescription() {
    const route = useRoute<RouteProp<StackParamList, 'ThesisDescription'>>();
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
                <Text style={styles.textBox}>Pobieranie danych...</Text>
            </View>
        );
    }

    const supervisor = thesis.supervisor_id.user;
    const fullName = `${supervisor.academic_title} ${supervisor.first_name} ${supervisor.last_name}`;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Tytuł pracy</Text>
                <Text style={styles.textBox}>{thesis.name}</Text>

                <Text style={styles.titleTextBox}>Promotor</Text>
                <Text style={styles.textBox}>{fullName}</Text>

                <Text style={styles.titleTextBox}>Dostępność</Text>
                <Text style={styles.textBox}>
                    Dostępne miejsca: <Text style={styles.slotValue}>x</Text> Zajęte miejsca:{' '}
                    <Text style={styles.slotValue}>y</Text> Oczekujące zgłoszenia:{' '}
                    <Text style={styles.slotValue}>z</Text>
                </Text>
            </View>

            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Opis pracy</Text>
                <Text style={styles.textBox}>{thesis.description}</Text>

                <TouchableOpacity
                    style={styles.signInButton}
                    onPress={() => console.log('Button pressed!')}
                >
                    <Text style={styles.buttonText}>Zapisz się</Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
}
