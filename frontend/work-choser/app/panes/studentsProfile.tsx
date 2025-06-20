import { styles } from '@/constants/styles';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { useCallback, useState } from 'react';
import { useFocusEffect } from 'expo-router';
import { getUserDataById } from '@/api/getUserDataById';

type Props = {
    id: number;
};

export default function StudentsProfile({ id }: Props) {
    const [description, setDescription] = useState('');
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [department, setDepartment] = useState('');

    useFocusEffect(
        useCallback(() => {
            let isActive = true;

            const fetchUser = async () => {
                try {
                    const data = await getUserDataById(id);
                    if (isActive) {
                        setFirstName(data.first_name);
                        setLastName(data.last_name);
                        setDepartment(data.department_name);
                        setDescription(data.description ?? 'Brak opisu');
                        setSelectedTags(Array.isArray(data.tags) ? data.tags : []);
                    }
                } catch (error) {
                    console.error('Błąd podczas pobierania danych studenta:', error);
                }
            };

            fetchUser();

            return () => {
                isActive = false;
            };
        }, [id]),
    );

    return (
        <ScrollView style={styles.container}>
            <View style={styles.narrowBox}>
                <Text style={styles.titleTextBox}>
                    {firstName} {lastName}
                </Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Wydział</Text>
                <Text style={styles.textBox}>{department}</Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Praca dyplomowa</Text>
                <Text style={styles.textBox}>Brak danych</Text>
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tagi</Text>
                </TouchableOpacity>

                {isTagsOpen && selectedTags.length > 0 ? (
                    <View style={styles.tagList}>
                        {selectedTags.map((tag, index) => (
                            <View key={index} style={styles.tagItem}>
                                <Text>{tag}</Text>
                            </View>
                        ))}
                    </View>
                ) : (
                    <Text style={styles.textBox}>Brak tagów</Text>
                )}
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Opis</Text>
                <Text style={styles.textBoxNotCentered}>{description}</Text>
            </View>
        </ScrollView>
    );
}
