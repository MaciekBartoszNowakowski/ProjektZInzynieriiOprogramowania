import { styles } from '@/constants/styles';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { useState } from 'react';
import tagName from '@/dummy_data/tagName.json';

export default function StudentsProfile() {
    const [description, setDescription] = useState('');
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [selectedTags, setSelectedTags] = useState<string[]>([]);

    const toggleTag = (tag: string) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
        } else {
            setSelectedTags((prev) => [...prev, tag]);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.narrowBox}>
                <Text style={styles.titleTextBox}>Grzegorz Grzęczyszczykiewicz</Text>
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Department</Text>
                <Text style={styles.textBox}>Computer Science Department</Text>
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
