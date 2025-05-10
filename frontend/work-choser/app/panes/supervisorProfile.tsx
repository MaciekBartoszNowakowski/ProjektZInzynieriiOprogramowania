import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import { useEffect, useState } from 'react';
import { useRoute, RouteProp } from '@react-navigation/native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import thesisTitle from '@/dummy_data/thesisTitle.json';

type Params = {
    SupervisorProfile: {
        name: string;
    };
};

type StackParamList = {
    ThesisDescription: { title: string; supervisor: string };
};

export default function SupervisorProfile() {
    const route = useRoute<RouteProp<Params, 'SupervisorProfile'>>();
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();
    const { name } = route.params;

    const [thesises, setThesis] = useState<{ title: string; supervisor: string }[]>([]);

    useEffect(() => {
        const filtered = thesisTitle.filter((t) => t.supervisor === name);
        setThesis(filtered);
    }, [name]);

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>{name}</Text>
                <Text style={styles.textBox}>Computer Science Department</Text>
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tags</Text>
                <Text style={styles.textBox}>#Machine learning, #AI, #LLM etc.</Text>
            </View>
            <View style={styles.container}>
                <Text style={styles.pageTitile}>List of Supervisor's Thesises</Text>
                {thesises.map((thesis, index) => (
                    //   <View key={index} style={styles.supervisorBox}>
                    //     <Text style={styles.titleTextBox}>{thesis.title}</Text>
                    //     <Text style={styles.textBox}>Supervisor: {thesis.supervisor}</Text>
                    //     <Text style={styles.textBox}>Available slots, occupied slots, pending slots</Text>
                    //   </View>
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
            </View>
            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
