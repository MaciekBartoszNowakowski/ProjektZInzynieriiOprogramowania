import { useRoute, RouteProp } from '@react-navigation/native';
import { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { getThesisById } from '@/api/getThesisById';
import { StackParamList } from '@/types/navigationTypes';
import { submitThesisApplication } from '@/api/submitThesisApplication';
import { showMessage } from '@/utils/showMessage';

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
                    Ilość miejsc: <Text style={styles.slotValue}>{thesis.max_students}</Text>
                </Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tagi</Text>
                <View style={styles.tagList}>
                    {Array.isArray(thesis.tags) ? (
                        thesis.tags.map((tag: string, index: number) => (
                            <View key={index} style={styles.tagItem}>
                                <Text style={styles.tagItem}>{tag}</Text>
                            </View>
                        ))
                    ) : (
                        <Text style={styles.textBox}>—</Text>
                    )}
                </View>
            </View>

            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Opis pracy</Text>
                <Text style={styles.textBoxNotCentered}>{thesis.description}</Text>

                <TouchableOpacity
                    style={styles.signInButton}
                    onPress={async () => {
                        const result = await submitThesisApplication(thesisId);

                        if (result.success) {
                            showMessage('Sukces', 'Zgłoszono się pomyślnie do pracy!');
                        } else {
                            const err = result.error;
                            const msg =
                                typeof err === 'string' ? err : err?.error || 'Nieznany błąd';

                            if (msg.includes('już zapisany')) {
                                showMessage('Nie można się zapisać', 'Masz już przypisaną pracę.');
                            } else if (msg.includes('APP_OPEN')) {
                                showMessage(
                                    'Nie można się zapisać',
                                    'Praca nie jest dostępna do zapisów.',
                                );
                            } else {
                                showMessage('Błąd', `Nie udało się zapisać:\n${msg}`);
                            }
                        }
                    }}
                >
                    <Text style={styles.buttonText}>Zapisz się</Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
}
