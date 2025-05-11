import { View, Text, FlatList, TouchableOpacity } from 'react-native';
import { styles } from '@/constants/styles';

const pendingStudents = [
    'Jan Kowalski',
    'Anna Nowak',
    'Tomasz Zieliński',
    'Maria Wiśniewska',
    'Piotr Kaczmarek',
];

export default function PendingStudentList() {
    return (
        <View style={styles.mainStudentListBox}>
            <Text style={styles.titleStudentListText}>Pending Students</Text>

            <FlatList
                data={pendingStudents}
                keyExtractor={(item, index) => `${item}-${index}`}
                renderItem={({ item }) => (
                    <View style={styles.singleElementFormStudentList}>
                        <Text style={styles.textBox}>{item}</Text>

                        <View style={styles.flexViewStyle}>
                            <TouchableOpacity
                                style={styles.signInButton}
                                onPress={() => console.log(`Accepted: ${item}`)}
                            >
                                <Text style={styles.buttonText}>Accept</Text>
                            </TouchableOpacity>

                            <TouchableOpacity
                                style={styles.declineButton}
                                onPress={() => console.log(`Declined: ${item}`)}
                            >
                                <Text style={styles.buttonText}>Decline</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                )}
            />
        </View>
    );
}
