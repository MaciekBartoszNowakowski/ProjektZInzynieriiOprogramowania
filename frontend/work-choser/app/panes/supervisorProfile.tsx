import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { useEffect, useState } from 'react';
import { useRoute, RouteProp } from '@react-navigation/native';
import { getAllTheses } from '@/api/getAllTheses';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { StackParamList } from '@/types/navigationTypes';
import { getUserDataById } from '@/api/getUserDataById';

export default function SupervisorProfile() {
    const route = useRoute<RouteProp<StackParamList, 'SupervisorProfile'>>();
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();
    const { id } = route.params;
    const [supervisor, setSupervisor] = useState<
        (SupervisorUser & { department_name?: string; tags?: string[] }) | null
    >(null);
    const [thesises, setThesises] = useState<any[]>([]);

    type SupervisorUser = {
        academic_title: string;
        first_name: string;
        last_name: string;
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [userData, allTheses] = await Promise.all([
                    getUserDataById(id),
                    getAllTheses(),
                ]);

                console.log('Supervisor data:', userData);
                console.log('All theses:', allTheses);
                setSupervisor(userData);

                const filteredTheses = allTheses.filter(
                    (thesis: any) => String(thesis.supervisor_id) === String(id),
                );
                setThesises(filteredTheses);
            } catch (error) {
                console.error('Error fetching supervisor or theses:', error);
            }
        };

        fetchData();
    }, [id]);

    if (!supervisor) {
        return (
            <View style={styles.container}>
                <Text style={styles.textBox}>Trwa pobieranie danych</Text>
            </View>
        );
    }
    const fullName = `${supervisor.academic_title} ${supervisor.first_name} ${supervisor.last_name}`;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>{fullName}</Text>
                <Text style={styles.textBox}>Wydział: {supervisor.department_name ?? '—'}</Text>
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tagi</Text>
                <View style={styles.tagList}>
                    {Array.isArray(supervisor.tags) ? (
                        supervisor.tags.map((tag: string, index: number) => (
                            <View key={index} style={styles.tagItem}>
                                <Text style={styles.tagItem}>{tag}</Text>
                            </View>
                        ))
                    ) : (
                        <Text style={styles.textBox}>—</Text>
                    )}
                </View>
            </View>

            <View style={styles.container}>
                <Text style={styles.pageTitile}>Lista wszystkich prac promotora</Text>
                {thesises.length > 0 ? (
                    thesises.map((thesis, index) => (
                        <TouchableOpacity
                            key={index}
                            style={styles.supervisorBox}
                            onPress={() => {
                                const thesisId = parseInt(
                                    thesis.url.split('/').filter(Boolean).pop() ?? '',
                                    10,
                                );
                                navigation.navigate('ThesisDescription', { thesisId });
                            }}
                        >
                            <Text style={styles.titleTextBox}>{thesis.name}</Text>
                            <Text style={styles.textBox}>{thesis.description}</Text>
                        </TouchableOpacity>
                    ))
                ) : (
                    <Text style={styles.textBox}>
                        Prowadzący aktualnie nie udostępnia prac dyplomowych
                    </Text>
                )}
            </View>
            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
