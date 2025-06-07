import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeProfile from '../panes/homeProfile';
import ThesisOwnerDescription from '../panes/thesisOwnerDescription';
import ThesisDescription from '../panes/thesisDescription';
import StudentsProfile from '../panes/studentsProfile';
import ApplicatedThesisDescription from '../panes/applicatedThesisDescription';
import AddingThesis from '../panes/addingThesis';
import NoActiveTheses from '../panes/noActiveThesis';
const Stack = createNativeStackNavigator();

export default function HomeStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="HomeProfile"
                component={HomeProfile}
                options={{ title: 'Strona główna' }}
            />
            <Stack.Screen
                name="ThesisOwnerDescription"
                component={ThesisOwnerDescription}
                options={{ title: 'Opis pracy dyplomowej' }}
            />
            <Stack.Screen
                name="ThesisDescription"
                component={ThesisDescription}
                options={{ title: 'Opis pracy dyplomowej' }}
            />
            <Stack.Screen name="StudentProfile" options={{ title: 'Profil studenta' }}>
                {({ route }) => <StudentsProfile id={Number(route.params.id)} />}
            </Stack.Screen>
            <Stack.Screen
                name="applicatedThesisDescription"
                component={ApplicatedThesisDescription}
                options={{ title: 'Moja praca dyplomowa' }}
            />
            <Stack.Screen
                name="AddingThesis"
                component={AddingThesis}
                options={{ title: 'Nowa praca dyplomowa' }}
            />
            <Stack.Screen
                name="noActiveThesis"
                component={NoActiveTheses}
                options={{ title: 'Opis pracy dyplomowej' }}
            />
        </Stack.Navigator>
    );
}
