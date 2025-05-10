import { styles } from '@/constants/styles';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { useCallback, useState } from 'react';
import tagName from '@/dummy_data/tagName.json';
import { useFocusEffect, useLocalSearchParams } from 'expo-router';
import { getUserDataById } from '@/api/getUserDataById';

export default function HomeStudentProfile() {
    const { id } = useLocalSearchParams();
    const userId = typeof id === 'string' ? id : null;

    const [description, setDescription] = useState('');
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [department, setDepartment] = useState(0);

    useFocusEffect(
        useCallback(() => {
            let isActive = true;

            const fetchUser = async () => {
                if (!userId) return;

                try {
                    const data = await getUserDataById(userId);
                    if (isActive) {
                        setFirstName(data.first_name);
                        setLastName(data.last_name);
                        setDepartment(data.department);
                        setDescription(data.description);
                        setSelectedTags(data.tags);
                    }
                } catch (error) {
                    console.error('Błąd:', error);
                }
            };

            fetchUser();

            return () => {
                isActive = false;
            };
        }, [userId]),
    );

    return (
        <ScrollView style={styles.container}>
            <View style={styles.narrowBox}>
                <Text style={styles.titleTextBox}>
                    {firstName} {lastName}
                </Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Department</Text>
                <Text style={styles.textBox}>{department}</Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Grades</Text>
                <Text style={styles.textBox}>Brak danych</Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Diploma Thesis</Text>
                <Text style={styles.textBox}>Brak danych</Text>
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tags</Text>
                </TouchableOpacity>

                {isTagsOpen && (
                    <View style={styles.tagList}>
                        {tagName.map((tag, index) => (
                            <View
                                key={index}
                                style={[
                                    styles.tagItem,
                                    selectedTags.includes(tag.name) && styles.tagItemSelected,
                                ]}
                            >
                                <Text>{tag.name}</Text>
                            </View>
                        ))}
                    </View>
                )}

                {selectedTags.length > 0 && (
                    <View style={styles.selectedTagsBox}>
                        {selectedTags.map((tag, index) => (
                            <Text key={index} style={styles.selectedTagText}>
                                {tag}
                            </Text>
                        ))}
                    </View>
                )}
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Description</Text>
                <Text style={styles.textBox}>{description || 'Brak opisu'}</Text>
            </View>
        </ScrollView>
    );
}
