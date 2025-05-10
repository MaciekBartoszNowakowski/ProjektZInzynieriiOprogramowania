import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { useState, useCallback } from 'react';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { getAllUsersPromotorsFilter } from '@/api/getAllUsersPromotorsFilter';
import { getAllTags } from '@/api/getAllTags';
import { getAllDepartments } from '@/api/getAllDepartments';
import { User } from '@/types/user';

type StackParamList = {
    SupervisorProfile: { id: number };
};

export default function SupervisorsList() {
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();

    const [isDepartmentsOpen, setIsDepartmentsOpen] = useState(false);
    const [selectedDepartments, setSelectedDepartment] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [availableTags, setAvailableTags] = useState<{ id: number; name: string }[]>([]);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [availableDepartments, setAvailableDepartments] = useState<
        { id: number; name: string }[]
    >([]);
    const [supervisors, setSupervisors] = useState<User[]>([]);
    const fetchPromotors = async (useFilters = false) => {
        const params: Record<string, any> = {
            role: 'supervisor',
            limit: 20,
        };

        if (useFilters) {
            if (selectedTags.length > 0) {
                params.tags = selectedTags;
            }
            if (selectedDepartments.length > 0) {
                params.department = selectedDepartments[0];
            }
        }

        const users = await getAllUsersPromotorsFilter(params);
        setSupervisors(users);
    };
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

            fetchPromotors(false);
            fetchTags();
            fetchDepartments();

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

            <TouchableOpacity
                style={styles.applyFiltersButton}
                onPress={() => fetchPromotors(true)}
            >
                <Text style={styles.buttonText}>Apply filters</Text>
            </TouchableOpacity>

            <Text style={styles.pageTitile}>List of Supervisors</Text>

            {supervisors.map((supervisor, index) => (
                <TouchableOpacity
                    key={index}
                    style={styles.supervisorBox}
                    onPress={() => {
                        console.log('supervisor:', supervisor);
                        navigation.navigate('SupervisorProfile', { id: supervisor.id });
                    }}
                >
                    <Text style={styles.titleTextBox}>
                        {supervisor.academic_title} {supervisor.first_name} {supervisor.last_name}
                    </Text>
                    <Text style={styles.textBox}>
                        Department: {supervisor.department_name ?? '—'}
                    </Text>
                    <Text style={styles.textBox}>
                        Tags: {Array.isArray(supervisor.tags) ? supervisor.tags.join(', ') : '—'}
                    </Text>
                </TouchableOpacity>
            ))}

            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
