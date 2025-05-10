import { View, Text, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { useEffect, useState } from 'react';
import { useRoute, RouteProp } from '@react-navigation/native';
// import { useNavigation } from '@react-navigation/native';
// import { NativeStackNavigationProp } from '@react-navigation/native-stack';

import { getUserDataById } from '@/api/getUserDataById';

type StackParamList = {
    SupervisorProfile: { url: string };
};

export default function SupervisorProfile() {
    const route = useRoute<RouteProp<StackParamList, 'SupervisorProfile'>>();
    const { url } = route.params;
    const [supervisor, setSupervisor] = useState(null);
    // const [thesises, setThesis] = useState<{ title: string; supervisor: string }[]>([]);

    useEffect(() => {
        const fetchDetails = async () => {
            const id = url.split('/').filter(Boolean).pop();
            if (!id) return;

            try {
                const data = await getUserDataById(id);
                setSupervisor(data);
            } catch (error) {
                console.error('Error fetching supervisor details:', error);
            }
        };

        fetchDetails();
    }, [url]);

    const fullName = `${supervisor.academic_title} ${supervisor.first_name} ${supervisor.last_name}`;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>{fullName}</Text>
                <Text style={styles.textBox}>Department: {supervisor.department_name ?? '—'}</Text>
            </View>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tags</Text>
                <View style={styles.tagList}>
                    {Array.isArray(supervisor.tags) ? (
                        supervisor.tags.map((tag: string, index: number) => (
                            <View key={index} style={styles.tagItem}>
                                <Text style={styles.tagText}>{tag}</Text>
                            </View>
                        ))
                    ) : (
                        <Text style={styles.textBox}>—</Text>
                    )}
                </View>
            </View>

            {/* <View style={styles.container}>
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
            </View> */}
            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
