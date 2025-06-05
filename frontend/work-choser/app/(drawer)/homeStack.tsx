import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeProfile from '../panes/homeProfile';
import ThesisOwnerDescription from '../panes/thesisOwnerDescription';
import ThesisDescription from '../panes/thesisDescription';
import StudentsProfile from '../panes/studentsProfile';

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
        </Stack.Navigator>
    );
}
