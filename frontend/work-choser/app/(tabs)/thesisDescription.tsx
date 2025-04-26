import {View, Text, TouchableOpacity, ScrollView} from 'react-native';
import { styles } from '@/constants/styles';

export default function ThesisDescription() {
    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Thesis Title</Text>
                <Text style={styles.textBox}>Title of the thesis</Text>
                <Text style={styles.titleTextBox}>Thesis Supervisor</Text>
                <Text style={styles.textBox}>Sławek Surowiec</Text>
                <Text style={styles.titleTextBox}>Availability</Text>
                <Text style={styles.textBox}>
                Free slots: <Text style={styles.slotValue}>x</Text>  Busy slots: <Text style={styles.slotValue}>y</Text>  Pending slots: <Text style={styles.slotValue}>z</Text>
                </Text>
            </View>
            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Thesis Description</Text>
                <Text style={styles.textBox}>Description of the thesis</Text>
                <TouchableOpacity style={styles.signInButton} onPress={() => console.log('Button pressed!')}>
                    <Text style={styles.buttonText}>Sign Up</Text>
                </TouchableOpacity>
            </View>
        </ScrollView>
        
    );
}