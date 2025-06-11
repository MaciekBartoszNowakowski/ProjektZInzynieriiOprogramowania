import { useRoute, RouteProp } from '@react-navigation/native';
import { ScrollView, View, Text } from 'react-native';
import { styles } from '@/constants/styles';
import { StackParamList } from '@/types/navigationTypes';

export default function ApplicatedThesisDescription() {
    const route = useRoute<RouteProp<StackParamList, 'applicatedThesisDescription'>>();
    const { name, supervisor, status, description } = route.params;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Tytuł Twojej pracy</Text>
                <Text style={styles.textBox}>{name}</Text>

                <Text style={styles.titleTextBox}>Promotor</Text>
                <Text style={styles.textBox}>{supervisor}</Text>

                <Text style={styles.titleTextBox}>Status przypisania</Text>
                <Text style={styles.textBox}>{status}</Text>
            </View>

            <View style={styles.thesisDescriptionBox}>
                <Text style={styles.titleTextBox}>Opis pracy</Text>
                <Text style={styles.textBox}>{description}</Text>
            </View>
        </ScrollView>
    );
}
