import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { showMessage } from '@/utils/showMessage';
import { useNavigation } from '@react-navigation/native';
import { addThesis } from '@/api/addThesis';

export default function AddingThesis() {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [isLanguageOpen, setIsLanguageOpen] = useState(false);
    const [isSlotsOpen, setIsSlotsOpen] = useState(false);
    const [language, setLanguage] = useState<'Polish' | 'English'>('Polish');
    const [maxStudents, setMaxStudents] = useState(1);
    const [isTypeOpen, setIsTypeOpen] = useState(false);
    const [type, setType] = useState<'licencjacka' | 'inżynierska' | 'magisterska' | 'doktorska'>(
        'inżynierska',
    );

    const typeLabelMap: Record<typeof type, string> = {
        licencjacka: 'Licencjacka',
        inżynierska: 'Inżynierska',
        magisterska: 'Magisterska',
        doktorska: 'Doktorska',
    };

    const navigation = useNavigation();

    const handleSubmit = async () => {
        const payload = {
            name,
            description,
            max_students: maxStudents,
            language,
            thesis_type: type,
        };

        const result = await addThesis(payload);

        if (result.success) {
            showMessage('Sukces', 'Praca została dodana.');
            navigation.goBack();
        } else {
            showMessage('Błąd', result.error);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Tytuł pracy</Text>
                <TextInput value={name} onChangeText={setName} style={styles.textBox} />
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Opis</Text>
                <TextInput
                    value={description}
                    onChangeText={setDescription}
                    style={styles.textBox}
                    multiline
                />
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTypeOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>
                        {isTypeOpen ? 'Ukryj typy prac' : 'Wybierz typ pracy'}
                    </Text>
                </TouchableOpacity>

                <Text style={styles.textBox}>Wybrano: {typeLabelMap[type]}</Text>

                {isTypeOpen && (
                    <View style={styles.filterList}>
                        {(['licencjacka', 'inżynierska', 'magisterska', 'doktorska'] as const).map(
                            (val) => (
                                <TouchableOpacity
                                    key={val}
                                    style={[
                                        styles.filterItem,
                                        type === val && styles.filterItemSelected,
                                    ]}
                                    onPress={() => setType(val)}
                                >
                                    <Text>{typeLabelMap[val]}</Text>
                                </TouchableOpacity>
                            ),
                        )}
                    </View>
                )}
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsLanguageOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>
                        {isLanguageOpen ? 'Ukryj języki' : 'Wybierz język'}
                    </Text>
                </TouchableOpacity>

                <Text style={styles.textBox}>
                    Wybrany język: {language === 'Polish' ? 'Język polski' : 'Język angielski'}
                </Text>

                {isLanguageOpen && (
                    <View style={styles.filterList}>
                        <TouchableOpacity
                            style={[
                                styles.filterItem,
                                language === 'Polish' && styles.filterItemSelected,
                            ]}
                            onPress={() => setLanguage('Polish')}
                        >
                            <Text>Język polski</Text>
                        </TouchableOpacity>
                        <TouchableOpacity
                            style={[
                                styles.filterItem,
                                language === 'English' && styles.filterItemSelected,
                            ]}
                            onPress={() => setLanguage('English')}
                        >
                            <Text>Język angielski</Text>
                        </TouchableOpacity>
                    </View>
                )}
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsSlotsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>
                        {isSlotsOpen ? 'Ukryj ilość miejsc' : 'Wybierz ilość miejsc'}
                    </Text>
                </TouchableOpacity>

                <Text style={styles.textBox}>Wybrano: {maxStudents} miejsc</Text>

                {isSlotsOpen && (
                    <View style={styles.filterList}>
                        {[1, 2, 3, 4, 5].map((val) => (
                            <TouchableOpacity
                                key={val}
                                style={[
                                    styles.filterItem,
                                    maxStudents === val && styles.filterItemSelected,
                                ]}
                                onPress={() => setMaxStudents(val)}
                            >
                                <Text>{val}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                )}
            </View>

            <TouchableOpacity onPress={handleSubmit} style={styles.signInButton}>
                <Text style={styles.buttonText}>Dodaj pracę</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}
