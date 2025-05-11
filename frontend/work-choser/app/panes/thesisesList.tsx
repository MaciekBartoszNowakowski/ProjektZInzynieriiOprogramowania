import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { useCallback, useState } from 'react';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { getAllTags } from '@/api/getAllTags';
import { getAllDepartments } from '@/api/getAllDepartments';
import { getAllTheses } from '@/api/getAllTheses';
import { getAllUsersPromotors } from '@/api/getAllUsersPromotors';
import { thesis_type } from '@/custom_enums/thesis_type';
import { searchTheses } from '@/api/searchTheses';

type ThesisesListStackParamList = {
    ThesisesList: undefined;
    ThesisDescription: { thesisId: number };
};

export default function ThesisesList() {
    const navigation = useNavigation<NativeStackNavigationProp<ThesisesListStackParamList>>();

    const [isDepartmentsOpen, setIsDepartmentsOpen] = useState(false);
    const [selectedDepartments, setSelectedDepartment] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [availableTags, setAvailableTags] = useState<{ id: number; name: string }[]>([]);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [availableDepartments, setAvailableDepartments] = useState<
        { id: number; name: string }[]
    >([]);
    const [availableTheses, setAvaliableTheses] = useState<
        {
            thesis_type: any;
            id: number;
            name: string;
            url: string;
            supervisor_id: number;
        }[]
    >([]);
    const [promotorsMap, setPromotorsMap] = useState<Record<number, string>>({});
    const [availableThesisTypes, setAvailableThesisTypes] = useState<string[]>([]);
    const [selectedThesisTypes, setSelectedThesisTypes] = useState<string[]>([]);
    const [isThesisTypesOpen, setIsThesisTypesOpen] = useState(false);

    useFocusEffect(
        useCallback(() => {
            let isActive = true;
            console.log('isActive: ', isActive);
            setSelectedTags([]);
            setSelectedDepartment([]);
            const fetchTags = async () => {
                try {
                    const data = await getAllTags();
                    setAvailableTags(data);
                } catch (error) {
                    console.error('Error while fetching tags: ', error);
                }
            };

            const fetchDepartments = async () => {
                try {
                    const data = await getAllDepartments();
                    setAvailableDepartments(data);
                } catch (error) {
                    console.error('Error while fetching departments:', error);
                }
            };

            const fetchTheses = async () => {
                try {
                    const data = await getAllTheses();
                    console.log('All theses:', data);
                    setAvaliableTheses(data);
                } catch (error) {
                    console.error('Error while fetching theses:', error);
                }
            };
            const fetchPromotors = async () => {
                try {
                    const allUsers = await getAllUsersPromotors();
                    const map: Record<number, string> = {};

                    allUsers.forEach((user: any) => {
                        if (user.role?.toLowerCase() === 'promotor') {
                            const idStr = user.url?.split('/').filter(Boolean).pop();
                            const id = parseInt(idStr ?? '', 10);

                            if (!isNaN(id)) {
                                map[id] =
                                    `${user.academic_title} ${user.first_name} ${user.last_name}`;
                            } else {
                                console.warn('Invalid ID in URL:', user.url);
                            }
                        }
                    });

                    setPromotorsMap(map);
                } catch (error) {
                    console.error('Error while fetching promotors:', error);
                }
            };

            fetchTheses();
            fetchTags();
            fetchDepartments();
            fetchPromotors();
            setAvailableThesisTypes(Object.keys(thesis_type));
            return () => {
                isActive = false;
            };
        }, []),
    );

    const toggleTag = (tag: string) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
        } else {
            setSelectedTags((prev) => [...prev, tag]);
        }
    };

    const toggleDepartment = (department: string) => {
        if (selectedDepartments.includes(department)) {
            setSelectedDepartment((prev) => prev.filter((d) => d !== department));
        } else {
            setSelectedDepartment((prev) => [...prev, department]);
        }
    };

    const toggleThesisType = (type: string) => {
        if (selectedThesisTypes.includes(type)) {
            setSelectedThesisTypes((prev) => prev.filter((t) => t !== type));
        } else {
            setSelectedThesisTypes((prev) => [...prev, type]);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <Text style={styles.pageTitile}>Filters</Text>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsDepartmentsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>
                        {isDepartmentsOpen ? 'Hide Departments' : 'Show Departments'}
                    </Text>
                </TouchableOpacity>

                {selectedDepartments.length > 0 && (
                    <View style={styles.selectedFilters}>
                        {selectedDepartments.map((dep, index) => (
                            <Text key={index} style={styles.selectedTagText}>
                                {dep}
                            </Text>
                        ))}
                    </View>
                )}

                {isDepartmentsOpen && (
                    <View style={styles.filterList}>
                        {availableDepartments.map((dept, index) => (
                            <TouchableOpacity
                                key={index}
                                onPress={() => toggleDepartment(dept.name)}
                                style={[
                                    styles.filterItem,
                                    selectedDepartments.includes(dept.name) &&
                                        styles.filterItemSelected,
                                ]}
                            >
                                <Text>{dept.name}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                )}
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity
                    onPress={() => setIsTagsOpen((prev) => !prev)}
                    style={styles.filterHeader}
                >
                    <Text style={styles.titleTextBox}>
                        {isTagsOpen ? 'Hide Tags' : 'Show Tags'}
                    </Text>
                </TouchableOpacity>

                {selectedTags.length > 0 && (
                    <View style={styles.selectedTagsBox}>
                        {selectedTags.map((tag, index) => (
                            <Text key={index} style={styles.selectedTagText}>
                                {tag}
                            </Text>
                        ))}
                    </View>
                )}

                {isTagsOpen && (
                    <View style={styles.tagList}>
                        {availableTags.map((tag, index) => (
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
            </View>
            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsThesisTypesOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>
                        {isThesisTypesOpen ? 'Hide Thesis Types' : 'Show Thesis Types'}
                    </Text>
                </TouchableOpacity>

                {selectedThesisTypes.length > 0 && (
                    <View style={styles.selectedFilters}>
                        {selectedThesisTypes.map((type, index) => (
                            <Text key={index} style={styles.selectedTagText}>
                                {thesis_type[type]}
                            </Text>
                        ))}
                    </View>
                )}

                {isThesisTypesOpen && (
                    <View style={styles.filterList}>
                        {availableThesisTypes.map((type, index) => (
                            <TouchableOpacity
                                key={index}
                                onPress={() => toggleThesisType(type)}
                                style={[
                                    styles.filterItem,
                                    selectedThesisTypes.includes(type) && styles.filterItemSelected,
                                ]}
                            >
                                <Text>{thesis_type[type]}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                )}
            </View>

            <TouchableOpacity
                style={styles.applyFiltersButton}
                onPress={async () => {
                    try {
                        const filtered = await searchTheses({
                            tags: selectedTags,
                            department: selectedDepartments[0],
                            thesis_type: selectedThesisTypes,
                        });
                        setAvaliableTheses(filtered);
                    } catch (error) {
                        console.error('Error while applying filters:', error);
                    }
                }}
            >
                <Text style={styles.buttonText}>Apply filters</Text>
            </TouchableOpacity>

            <Text style={styles.pageTitile}>List of Thesises</Text>
            {availableTheses.map((thesis, index) => {
                const thesisId = parseInt(thesis.url?.split('/').filter(Boolean).pop() ?? '', 10);
                return (
                    <TouchableOpacity
                        key={index}
                        style={styles.supervisorBox}
                        onPress={() => navigation.navigate('ThesisDescription', { thesisId })}
                    >
                        <Text style={styles.titleTextBox}>{thesis.name}</Text>
                        <Text style={styles.textBox}>
                            Supervisor: {promotorsMap[thesis.supervisor_id] ?? '—'}
                        </Text>
                        <Text style={styles.textBox}>
                            Thesis type: {thesis_type[thesis.thesis_type] ?? thesis.thesis_type}
                        </Text>
                    </TouchableOpacity>
                );
            })}

            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
