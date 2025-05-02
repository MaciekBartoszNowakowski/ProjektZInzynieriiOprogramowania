import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { useState } from 'react';

const thesisExample = [
    { name: 'Tram Newtork Simulation' },
    { name: 'AI in chemistry' },
    { name: 'AGH Guide' },
];

const departmentName = [{ name: 'WI' }, { name: 'WIET' }, { name: 'WEAIB' }];

const tagName = [
    { name: 'AI' },
    { name: 'ML' },
    { name: 'Security' },
    { name: 'Databases' },
    { name: 'WebDev' },
];

export default function ThesisesList() {
    const [isDepartmentsOpen, setIsDepartmentsOpen] = useState(false);
    const [selectedDepartments, setSelectedDepartments] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const toggleDepartment = (department: string) => {
        if (selectedDepartments.includes(department)) {
            setSelectedDepartments((prev) => prev.filter((dep) => dep !== department));
        } else {
            setSelectedDepartments((prev) => [...prev, department]);
        }
    };
    const toggleTag = (tag: string) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
        } else {
            setSelectedTags((prev) => [...prev, tag]);
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
                        {departmentName.map((dept, index) => (
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
            </View>

            <TouchableOpacity
                style={styles.applyFiltersButton}
                onPress={() => console.log('Button pressed!')}
            >
                <Text style={styles.buttonText}>Apply filters</Text>
            </TouchableOpacity>

            <Text style={styles.pageTitile}>List of Thesises</Text>
            {thesisExample.map((thesis, index) => (
                <View key={index} style={styles.supervisorBox}>
                    <Text key={index} style={styles.titleTextBox}>
                        {thesis.name}
                    </Text>
                    <Text style={styles.textBox}>Departament, tags, etc, supervisor</Text>
                </View>
            ))}
            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
