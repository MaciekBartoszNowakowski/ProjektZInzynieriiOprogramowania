import { useRoute, RouteProp } from '@react-navigation/native';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';
import thesisData from '@/dummy_data/thesisTitle.json';

type Params = {
    ThesisDescription: {
        title: string;
        supervisor: string;
    };
};

export default function ThesisDescription() {
    const route = useRoute<RouteProp<Params, 'ThesisDescription'>>();
    const { title } = route.params;

    const thesis = thesisData.find(
        (t) => t.title.trim().toLowerCase() === title.trim().toLowerCase(),
    );

    if (!thesis) {
        return (
            <View style={styles.container}>
                <Text style={styles.textBox}>Thesis not found</Text>
            </View>
        );
    }

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Thesis Title</Text>
                <Text style={styles.textBox}>{thesis.title}</Text>
                <Text style={styles.titleTextBox}>Supervisor</Text>
                <Text style={styles.textBox}>{thesis.supervisor}</Text>
                <Text style={styles.titleTextBox}>Availability</Text>
                <Text style={styles.textBox}>
                    Free slots: <Text style={styles.slotValue}>x</Text> Busy slots:{' '}
                    <Text style={styles.slotValue}>y</Text> Pending slots:{' '}
                    <Text style={styles.slotValue}>z</Text>
                </Text>
            </View>
            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Thesis Description</Text>
                <Text style={styles.textBox}>Description of the thesis</Text>
                <TouchableOpacity
                    style={styles.signInButton}
                    onPress={() => console.log('Button pressed!')}
                >
                    <Text style={styles.buttonText}>Sign Up</Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
}
