import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import { getUserDataById } from '@/api/getUserDataById';
import tagName from '@/dummy_data/tagName.json';

type Props = {
    id: string;
};

export default function HomeSupervisorProfile({ id }: Props) {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [academicTitle, setAcademicTitle] = useState('');
    const [department, setDepartment] = useState<number | null>(null);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);

    // const [thesises, setThesis] = useState<{ title: string; supervisor: string }[]>([]);

    useFocusEffect(
        useCallback(() => {
            let isActive = true;

            const fetchUser = async () => {
                try {
                    const data = await getUserDataById(id);
                    if (isActive && data) {
                        setFirstName(data.first_name);
                        setLastName(data.last_name);
                        setEmail(data.email);
                        setAcademicTitle(data.academic_title);
                        setDepartment(data.department);
                        setSelectedTags(data.tags ?? []);
                    }
                } catch (error) {
                    console.error('Błąd pobierania danych promotora:', error);
                }
            };

            fetchUser();
            return () => {
                isActive = false;
            };
        }, [id]),
    );

    const toggleTag = (tag: string) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
        } else {
            setSelectedTags((prev) => [...prev, tag]);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>
                    {academicTitle} {firstName} {lastName}
                </Text>
                <Text style={styles.textBox}>E-mail: {email || 'Brak'}</Text>
                <Text style={styles.textBox}>Department: {department ?? 'Brak'}</Text>
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tags</Text>
                </TouchableOpacity>

                {isTagsOpen && (
                    <View style={styles.tagList}>
                        {tagName.map((tag, index) => (
                            <TouchableOpacity
                                key={index}
                                onPress={() => toggleTag(tag.name)}
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

            {/* <View style={styles.container}>
        <Text style={styles.pageTitile}>List of Supervisor's Thesises</Text>
        {thesises.map((thesis, index) => (
          <TouchableOpacity
            key={index}
            style={styles.supervisorBox}
            onPress={() =>
              navigation.navigate('ThesisDescription', {
                title: thesis.title,
                supervisor: thesis.supervisor,
              })
            }
          >
            <Text style={styles.titleTextBox}>{thesis.title}</Text>
            <Text style={styles.textBox}>Supervisor: {thesis.supervisor}</Text>
          </TouchableOpacity>
        ))}
      </View> */}

            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
