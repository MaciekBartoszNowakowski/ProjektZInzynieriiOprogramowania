import { styles } from '@/constants/styles';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { useCallback, useState } from 'react';
import { useFocusEffect } from 'expo-router';
import { getUserDataById } from '@/api/getUserDataById';
import { getAllTags } from '@/api/getAllTags';
import { updateTags } from '@/api/updateTags';

type Props = {
    id: string;
};

export default function homeStudentProfile({ id }: Props) {
    const [description, setDescription] = useState('');
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [department, setDepartment] = useState('');
    const [availableTags, setAvailableTags] = useState<{ id: number; name: string }[]>([]);

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
                        setDescription(data.description);
                        setSelectedTags(data.tags);
                    }
                } catch (error) {
                    console.error('Error while fetching user:', error);
                }
            };

            const fetchTags = async () => {
                try {
                    const data = await getAllTags();
                    setAvailableTags(data);
                    console.log('Tags: ', data);
                } catch (error) {
                    console.error('Error while fetching tags: ', error);
                }
            };

            fetchUser();
            fetchTags();

            return () => {
                isActive = false;
            };
        }, []),
    );

    const toggleTag = (tag: string, id: number) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
            updateTags([], [id.toString()]);
        } else {
            setSelectedTags((prev) => [...prev, tag]);
            updateTags([id.toString()], []);
        }
    };

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
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Diploma Thesis</Text>
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tags</Text>
                </TouchableOpacity>

                {isTagsOpen && (
                    <View style={styles.tagList}>
                        {availableTags.map((tag) => (
                            <TouchableOpacity
                                key={tag.id}
                                onPress={() => toggleTag(tag.name, tag.id)}
                                style={[
                                    styles.tagItem,
                                    selectedTags.includes(tag.name) && styles.tagItemSelected,
                                ]}
                            >
                                <Text>{tag.name}</Text>
                            </TouchableOpacity>
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
                <TextInput
                    style={styles.textBox}
                    placeholder="Enter your description..."
                    value={description}
                    onChangeText={setDescription}
                    multiline
                />
            </View>
        </ScrollView>
    );
}
