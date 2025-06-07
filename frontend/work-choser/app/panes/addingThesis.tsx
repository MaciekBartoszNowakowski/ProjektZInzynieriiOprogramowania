import { useEffect, useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { styles } from '@/constants/styles';
import { showMessage } from '@/utils/showMessage';
import { useNavigation } from '@react-navigation/native';
import { addThesis } from '@/api/addThesis';
import { getUserRole } from '@/api/getUserRole';
import { getMyTheses } from '@/api/getMyTheses';

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

    const [limits, setLimits] = useState({ bachelor: 0, engineering: 0, master: 0, phd: 0 });
    const [workload, setWorkload] = useState({ bachelor: 0, engineering: 0, master: 0, phd: 0 });

    useEffect(() => {
        const fetchLimitsAndWorkload = async () => {
            try {
                const user = await getUserRole();
                if (user) {
                    setLimits({
                        bachelor: user.bachelor_limit,
                        engineering: user.engineering_limit,
                        master: user.master_limit,
                        phd: user.phd_limit,
                    });
                }

                const theses = await getMyTheses();
                console.log('Pobrane prace:', theses);
                const workloadCount = { bachelor: 0, engineering: 0, master: 0, phd: 0 };
                theses
                    .filter((t: any) => t.status === 'otwarta' || t.status === 'w realizacji')
                    .forEach((t: any) => {
                        console.log('Przetwarzanie pracy:', t);
                        switch (t.thesis_type?.toLowerCase()) {
                            case 'licencjacka':
                                workloadCount.bachelor++;
                                break;
                            case 'inżynierska':
                                workloadCount.engineering++;
                                break;
                            case 'magisterska':
                                workloadCount.master++;
                                break;
                            case 'doktorska':
                                workloadCount.phd++;
                                break;
                        }
                    });

                setWorkload(workloadCount);
            } catch (err) {
                console.error('Błąd pobierania limitów i obciążenia:', err);
            }
        };

        fetchLimitsAndWorkload();
    }, []);

    const handleSubmit = async () => {
        const limitReached =
            (type === 'licencjacka' && workload.bachelor >= limits.bachelor) ||
            (type === 'inżynierska' && workload.engineering >= limits.engineering) ||
            (type === 'magisterska' && workload.master >= limits.master) ||
            (type === 'doktorska' && workload.phd >= limits.phd);

        if (limitReached) {
            showMessage(
                'Limit osiągnięty',
                `Nie możesz dodać więcej prac typu ${typeLabelMap[type]}.`,
            );
            return;
        }
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
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>Limity prac</Text>
                <Text style={styles.textBox}>
                    Licencjackie: {workload.bachelor} / {limits.bachelor}
                </Text>
                <Text style={styles.textBox}>
                    Inżynierskie: {workload.engineering} / {limits.engineering}
                </Text>
                <Text style={styles.textBox}>
                    Magisterskie: {workload.master} / {limits.master}
                </Text>
                <Text style={styles.textBox}>
                    Doktorskie: {workload.phd} / {limits.phd}
                </Text>
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Tytuł pracy</Text>
                <TextInput value={name} onChangeText={setName} style={styles.textBox} />
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Opis</Text>
                <TextInput
                    value={description}
                    onChangeText={setDescription}
                    style={styles.textBoxNotCentered}
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

            <TouchableOpacity onPress={handleSubmit} style={styles.addThesesButton}>
                <Text style={styles.buttonText}>Dodaj pracę</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}
