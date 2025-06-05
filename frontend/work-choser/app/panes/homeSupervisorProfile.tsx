import { View, Text, ScrollView, TouchableOpacity, TextInput } from 'react-native';
import { styles } from '@/constants/styles';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { useCallback, useEffect, useState } from 'react';
import { getUserDataById } from '@/api/getUserDataById';
import { getAllTags } from '@/api/getAllTags';
import { updateTags } from '@/api/updateTags';
import { changeDescription } from '@/api/changeDescription';
import { getAllTheses } from '@/api/getAllTheses';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { StackParamList } from '@/types/navigationTypes';

type Props = {
    id: string;
};

export default function HomeSupervisorProfile({ id }: Props) {
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();

    const [description, setDescription] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [academicTitle, setAcademicTitle] = useState('');
    const [department, setDepartment] = useState('');
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [availableTags, setAvailableTags] = useState<{ id: number; name: string }[]>([]);
    const [thesises, setThesises] = useState<any[]>([]);

    useFocusEffect(
        useCallback(() => {
            let isActive = true;

            const fetchUser = async () => {
                try {
                    const data = await getUserDataById(id);
                    const thesesData = await getAllTheses();

                    const filteredTheses = thesesData.filter(
                        (thesis: any) => String(thesis.supervisor_id) === String(id),
                    );
                    setThesises(filteredTheses);

                    if (isActive && data) {
                        setFirstName(data.first_name);
                        setLastName(data.last_name);
                        setEmail(data.email);
                        setAcademicTitle(data.academic_title);
                        setDepartment(data.department_name);
                        setSelectedTags(data.tags ?? []);
                        setDescription(data.description);
                    }
                } catch (error) {
                    console.error('Błąd pobierania danych promotora:', error);
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
        }, [id]),
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
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>
                    {academicTitle} {firstName} {lastName}
                </Text>
                <Text style={styles.textBox}>E-mail: {email || 'Brak'}</Text>
                <Text style={styles.textBox}>Wydział: {department ?? 'Brak'}</Text>
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
                    style={styles.textBox}
                    placeholder="Wprowadź swój opis..."
                    value={description}
                    onChangeText={setDescription}
                    multiline
                />
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity
                    style={styles.signInButton}
                    onPress={() => navigation.navigate('AddingThesis')}
                >
                    <Text style={styles.buttonText}>Dodaj pracę dyplomową</Text>
                </TouchableOpacity>
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
                                navigation.navigate('ThesisOwnerDescription', { thesisId });
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
