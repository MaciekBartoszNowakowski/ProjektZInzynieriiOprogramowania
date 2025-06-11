import { styles } from '@/constants/styles';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { useCallback, useEffect, useState } from 'react';
import { useFocusEffect } from 'expo-router';
import { getUserDataById } from '@/api/getUserDataById';
import { getAllTags } from '@/api/getAllTags';
import { updateTags } from '@/api/updateTags';
import { changeDescription } from '@/api/changeDescription';
import { getSubmissionStatus } from '@/api/getSubmissionStatus';
import { useNavigation } from '@react-navigation/native';
import { StackParamList } from '@/types/navigationTypes';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { cancelApplication } from '@/api/cancelApplication';

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
    const [thesisTitle, setThesisTitle] = useState<string | null>(null);
    const [thesisSupervisor, setThesisSupervisor] = useState<string | null>(null);
    const [thesisId, setThesisId] = useState<number | null>(null);
    const [applicationStatus, setApplicationStatus] = useState<string | null>(null);
    const [thesisDescription, setThesisDescription] = useState<string | null>(null);

    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();
    console.log('ID: ', id);
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

            const fetchThesisStatus = async () => {
                try {
                    const result = await getSubmissionStatus();
                    console.log('Submission status result:', result);
                    if (result.success && result.data.has_submission) {
                        const submissionStatus = result.data.submission.status;
                        setApplicationStatus(submissionStatus);
                        if (submissionStatus === 'odrzucone') {
                            try {
                                await cancelApplication();
                                setThesisTitle(null);
                                setThesisSupervisor(null);
                                setThesisId(null);
                                console.log('Odrzucona aplikacja została automatycznie usunięta.');
                            } catch (error) {
                                console.error('Błąd przy automatycznym usuwaniu aplikacji:', error);
                            }
                        } else {
                            setThesisTitle(result.data.submission.thesis.name);
                            setThesisSupervisor(result.data.submission.thesis.supervisor_name);
                            setThesisId(result.data.submission.thesis.id);
                            setThesisDescription(result.data.submission.thesis.description);
                        }
                    } else {
                        setThesisTitle(null);
                        setThesisSupervisor(null);
                        setThesisId(null);
                    }
                } catch (error) {
                    console.error('Błąd przy pobieraniu statusu pracy:', error);
                }
            };

            fetchUser();
            fetchTags();
            fetchThesisStatus();

            return () => {
                isActive = false;
            };
        }, []),
    );

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (description.trim()) {
                changeDescription(description);
            }
        }, 800);

        return () => clearTimeout(timeout);
    }, [description]);

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
                <Text style={styles.titleTextBox}>Wydział</Text>
                <Text style={styles.textBox}>{department}</Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Praca dyplomowa</Text>
                {thesisTitle ? (
                    <TouchableOpacity
                        onPress={() => {
                            if (thesisId !== null) {
                                navigation.navigate('applicatedThesisDescription', {
                                    thesisId,
                                    name: thesisTitle || 'brak danych',
                                    supervisor: thesisSupervisor || 'brak danych',
                                    status: applicationStatus || 'brak danych',
                                    description: thesisDescription || 'brak danych',
                                });
                            }
                        }}
                        style={styles.tagItem}
                    >
                        <Text style={styles.textBox}>Tytuł: {thesisTitle}</Text>
                        <Text style={styles.textBox}>Promotor: {thesisSupervisor}</Text>
                        {applicationStatus && (
                            <Text style={styles.textBox}>Status: {applicationStatus}</Text>
                        )}
                    </TouchableOpacity>
                ) : (
                    <Text style={styles.textBox}>Brak aktywnej aplikacji</Text>
                )}
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tagi</Text>
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
                <Text style={styles.titleTextBox}>Opis</Text>
                <TextInput
                    style={styles.textBoxNotCentered}
                    placeholder="Wprowadź swój opis..."
                    value={description}
                    onChangeText={setDescription}
                    multiline
                />
            </View>
        </ScrollView>
    );
}
