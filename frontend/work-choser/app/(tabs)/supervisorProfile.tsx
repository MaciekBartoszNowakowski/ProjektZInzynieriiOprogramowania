import { View, Text, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { useEffect, useState } from 'react';

const dummyData = [
    { name: 'LLM in medicine' },
    { name: 'ChatGPT in schools' },
    { name: 'Jedli pierogi a sufit byl nisko' },
];

export default function SupervisorProfile() {
    const [thesises, setThesis] = useState<{ name: string }[]>([]);
    useEffect(() => {
        setTimeout(() => {
            setThesis(dummyData);
        });
    }, []);

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Sławek Surowiec</Text>
                <Text style={styles.textBox}>Computer Science Department</Text>
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tags</Text>
                <Text style={styles.textBox}>#Machine learning, #AI, #LLM etc.</Text>
            </View>
            <View style={styles.container}>
                <Text style={styles.pageTitile}>List of Supervisor's Thesises</Text>
                {thesises.map((thesis, index) => (
                    <View key={index} style={styles.supervisorBox}>
                        <Text key={index} style={styles.titleTextBox}>
                            {thesis.name}
                        </Text>
                        <Text style={styles.textBox}>
                            avaliable slots, occupated slots, pending slots,
                        </Text>
                    </View>
                ))}
            </View>
            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
