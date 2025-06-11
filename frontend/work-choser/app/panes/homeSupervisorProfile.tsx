import { View, Text, ScrollView, TouchableOpacity, TextInput } from 'react-native';
import { styles } from '@/constants/styles';
import { useFocusEffect, useNavigation } from '@react-navigation/native';
import { useCallback, useEffect, useState } from 'react';
import { getUserDataById } from '@/api/getUserDataById';
import { getAllTags } from '@/api/getAllTags';
import { updateTags } from '@/api/updateTags';
import { changeDescription } from '@/api/changeDescription';
import { getAllTheses } from '@/api/getAllTheses';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { StackParamList } from '@/types/navigationTypes';
import { getThesisSubmissions } from '@/api/getThesisSubmissions';
import { getMyTheses } from '@/api/getMyTheses';
// import { deleteThesis } from '@/api/deleteThesis';
import { getUserRole } from '@/api/getUserRole';
type Props = {
    id: string;
};

export default function HomeSupervisorProfile({ id }: Props) {
    const navigation = useNavigation<NativeStackNavigationProp<StackParamList>>();

    const [description, setDescription] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [academicTitle, setAcademicTitle] = useState('');
    const [department, setDepartment] = useState('');
    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [isTagsOpen, setIsTagsOpen] = useState(false);
    const [availableTags, setAvailableTags] = useState<{ id: number; name: string }[]>([]);
    const [thesises, setThesises] = useState<{ [status: string]: any[] }>({});
    const [pendingCounts, setPendingCounts] = useState<{ [thesisId: number]: number }>({});
    const [limits, setLimits] = useState({
        bachelor: 0,
        engineering: 0,
        master: 0,
        phd: 0,
    });
    const [workload, setWorkload] = useState({
        bachelor: 0,
        engineering: 0,
        master: 0,
        phd: 0,
    });

    useFocusEffect(
        useCallback(() => {
            let isActive = true;

            const fetchUser = async () => {
                try {
                    const data = await getUserDataById(id);
                    const userRoleData = await getUserRole();

                    setLimits({
                        bachelor: userRoleData.bachelor_limit,
                        engineering: userRoleData.engineering_limit,
                        master: userRoleData.master_limit,
                        phd: userRoleData.phd_limit,
                    });
                    const [allTheses, myTheses] = await Promise.all([
                        getAllTheses(),
                        getMyTheses(),
                    ]);

                    const active = allTheses.filter(
                        (t: any) => String(t.supervisor_id) === String(id),
                    );
                    active.forEach((t: { status: string }) => {
                        t.status = 'aktywne';
                    });

                    const other = myTheses.filter(
                        (t: any) => t.status === 'w realizacji' || t.status === 'zakończona',
                    );
                    const relevant = [...active, ...other];
                    const activeAndInProgress = relevant.filter(
                        (t) => t.status === 'aktywne' || t.status === 'w realizacji',
                    );

                    const workloadCount = {
                        bachelor: 0,
                        engineering: 0,
                        master: 0,
                        phd: 0,
                    };

                    activeAndInProgress.forEach((thesis) => {
                        switch (thesis.thesis_type?.toLowerCase()) {
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

                    const counts: { [thesisId: number]: number } = {};
                    await Promise.all(
                        active.map(async (thesis: { url: string; id: any }) => {
                            try {
                                const idFromUrl = parseInt(
                                    thesis.url?.split('/').filter(Boolean).pop() ?? '',
                                    10,
                                );
                                console.log('ID z URL:', idFromUrl);
                                if (!isNaN(idFromUrl)) {
                                    const submissions = await getThesisSubmissions(idFromUrl);
                                    counts[idFromUrl] = submissions.filter(
                                        (s: any) => s.status === 'aktywne',
                                    ).length;
                                }
                            } catch (err) {
                                console.warn(
                                    `Błąd pobierania zgłoszeń dla pracy ID ${thesis.id}:`,
                                    err,
                                );
                            }
                        }),
                    );
                    setPendingCounts(counts);

                    const combined = [...active, ...other];

                    const grouped: { [status: string]: any[] } = {};
                    for (const thesis of combined) {
                        const status = thesis.status || 'nieznany';
                        if (!grouped[status]) grouped[status] = [];
                        grouped[status].push(thesis);
                    }

                    setThesises(grouped);

                    if (isActive && data) {
                        setFirstName(data.first_name);
                        setLastName(data.last_name);
                        setEmail(data.email);
                        setAcademicTitle(data.academic_title);
                        setDepartment(data.department_name);
                        setSelectedTags(data.tags ?? []);
                        setDescription(data.description);
                    }
                } catch (error) {
                    console.error('Błąd pobierania danych promotora:', error);
                }
            };

            const fetchTags = async () => {
                try {
                    const data = await getAllTags();
                    setAvailableTags(data);
                } catch (error) {
                    console.error('Error while fetching tags: ', error);
                }
            };

            fetchUser();
            fetchTags();

            return () => {
                isActive = false;
            };
        }, [id]),
    );

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (description.trim()) {
                changeDescription(description);
            }
        }, 800);

        return () => clearTimeout(timeout);
    }, [description]);

    const toggleTag = (tag: string, id: number) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags((prev) => prev.filter((t) => t !== tag));
            updateTags([], [id.toString()]);
        } else {
            setSelectedTags((prev) => [...prev, tag]);
            updateTags([id.toString()], []);
        }
    };

    const statusOrder = ['aktywne', 'w realizacji', 'zakończona'];

    return (
        <ScrollView style={styles.container}>
            <View style={styles.defaultBox}>
                <Text style={styles.titleTextBox}>
                    {academicTitle} {firstName} {lastName}
                </Text>
                <Text style={styles.textBox}>E-mail: {email || 'Brak'}</Text>
                <Text style={styles.textBox}>Wydział: {department ?? 'Brak'}</Text>
            </View>

            <View style={styles.defaultBox}>
                <TouchableOpacity onPress={() => setIsTagsOpen((prev) => !prev)}>
                    <Text style={styles.titleTextBox}>Tagi</Text>
                </TouchableOpacity>

                {isTagsOpen && (
                    <View style={styles.tagList}>
                        {availableTags.map((tag) => (
                            <TouchableOpacity
                                key={tag.id}
                                onPress={() => toggleTag(tag.name, tag.id)}
                                style={[
                                    styles.tagItem,
                                    selectedTags.includes(tag.name) && styles.tagItemSelected,
                                ]}
                            >
                                <Text>{tag.name}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                )}

                {selectedTags.length > 0 && (
                    <View style={styles.selectedTagsBox}>
                        {selectedTags.map((tag, index) => (
                            <Text key={index} style={styles.selectedTagText}>
                                {tag}
                            </Text>
                        ))}
                    </View>
                )}
            </View>

            <View style={styles.inputBox}>
                <Text style={styles.titleTextBox}>Opis</Text>
                <TextInput
                    style={styles.textBoxNotCentered}
                    placeholder="Wprowadź swój opis..."
                    value={description}
                    onChangeText={setDescription}
                    multiline
                />
            </View>
            <View style={styles.defaultBox}>
                <View style={styles.marginTop10}>
                    <Text style={styles.textBox}>
                        Prace Licencjackie: {workload.bachelor} /{' '}
                        {limits.bachelor + workload.bachelor}
                    </Text>
                    <Text style={styles.textBox}>
                        Prace Inżynierskie: {workload.engineering} /{' '}
                        {limits.engineering + workload.engineering}
                    </Text>
                    <Text style={styles.textBox}>
                        Prace Magisterskie: {workload.master} / {limits.master + workload.master}
                    </Text>
                    <Text style={styles.textBox}>
                        Prace Doktorskie: {workload.phd} / {limits.phd + workload.phd}
                    </Text>
                </View>
                <TouchableOpacity
                    style={styles.addThesesButton}
                    onPress={() => navigation.navigate('AddingThesis')}
                >
                    <Text style={styles.buttonText}>Dodaj pracę dyplomową</Text>
                </TouchableOpacity>
            </View>

            <Text style={styles.pageTitile}>Lista prac promotora według statusu</Text>

            {Object.entries(thesises)
                .sort(([a], [b]) => statusOrder.indexOf(a) - statusOrder.indexOf(b))
                .map(([status, group]) => (
                    <View key={status}>
                        <Text style={styles.subtitle}>{status.toUpperCase()}</Text>
                        {group.map((thesis: any) => {
                            const thesisId = parseInt(
                                thesis.url?.split('/').filter(Boolean).pop() ?? '',
                                10,
                            );

                            const count = pendingCounts[thesisId] ?? 0;
                            const dynamicColor = count > 0 ? styles.redText : styles.normalText;

                            return (
                                <TouchableOpacity
                                    key={thesisId}
                                    style={styles.supervisorBox}
                                    onPress={() => {
                                        if (status === 'w realizacji' || status === 'zakończona') {
                                            navigation.navigate('noActiveThesis', { thesis });
                                        } else {
                                            navigation.navigate('ThesisOwnerDescription', {
                                                thesisId,
                                            });
                                        }
                                    }}
                                >
                                    <Text style={styles.titleTextBox}>{thesis.name}</Text>
                                    <Text style={styles.textBox}>
                                        Tagi:{' '}
                                        {Array.isArray(thesis.tags) ? thesis.tags.join(', ') : '—'}
                                    </Text>
                                    <Text style={styles.textBox}>
                                        Typ pracy: {thesis.thesis_type}
                                    </Text>

                                    {status === 'aktywne' && (
                                        <>
                                            <Text style={[styles.textBox, dynamicColor]}>
                                                {count > 0
                                                    ? `${count} oczekujących zgłoszeń`
                                                    : 'Brak oczekujących zgłoszeń'}
                                            </Text>

                                            {/* <TouchableOpacity
                                                style={styles.deleteButton}
                                                onPress={() => handleDeleteThesis(thesisId)}
                                            >
                                                <Text style={styles.buttonText}>Usuń pracę</Text>
                                            </TouchableOpacity> */}
                                        </>
                                    )}
                                </TouchableOpacity>
                            );
                        })}
                    </View>
                ))}

            <View style={styles.freeSpace} />
        </ScrollView>
    );
}
