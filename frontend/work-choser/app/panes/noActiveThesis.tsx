import { useRoute, RouteProp } from '@react-navigation/native';
import { ScrollView, Text, View } from 'react-native';
import { styles } from '@/constants/styles';
import { StackParamList } from '@/types/navigationTypes';

export default function noActiveThesis() {
    const route = useRoute<RouteProp<StackParamList, 'noActiveThesis'>>();
    const { thesis } = route.params;

    return (
        <ScrollView style={styles.container}>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Tytuł pracy</Text>
                <Text style={styles.textBox}>{thesis.name}</Text>
            </View>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Typ pracy</Text>
                <Text style={styles.textBox}>{thesis.thesis_type}</Text>
            </View>

            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Tagi</Text>
                <View style={styles.tagList}>
                    {Array.isArray(thesis.tags) ? (
                        thesis.tags.map((tag: string, index: number) => (
                            <View key={index} style={styles.tagItem}>
                                <Text style={styles.tagItem}>{tag}</Text>
                            </View>
                        ))
                    ) : (
                        <Text style={styles.textBox}>—</Text>
                    )}
                </View>
            </View>

            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Opis pracy</Text>
                <Text style={styles.textBox}>{thesis.description}</Text>
            </View>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Język</Text>
                <Text style={styles.textBox}>{thesis.language}</Text>
            </View>
            <View style={styles.thesisTitleBox}>
                <Text style={styles.titleTextBox}>Maksymalna liczba studentów</Text>
                <Text style={styles.textBox}>{thesis.max_students}</Text>
            </View>
        </ScrollView>
    );
}
