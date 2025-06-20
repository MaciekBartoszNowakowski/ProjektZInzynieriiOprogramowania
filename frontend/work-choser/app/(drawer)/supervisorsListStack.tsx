import { createNativeStackNavigator } from '@react-navigation/native-stack';
import SupervisorList from '../panes/supervisorsList';
import SupervisorProfile from '../panes/supervisorProfile';
import ThesisDescription from '../panes/thesisDescription';
import StudentsProfile from '../panes/studentsProfile';

const Stack = createNativeStackNavigator();

export default function SupervisorsListStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="SupervisorsList"
                component={SupervisorList}
                options={{ title: 'Lista promotorów' }}
            />
            <Stack.Screen
                name="SupervisorProfile"
                component={SupervisorProfile}
                options={{ title: 'Profil promotora' }}
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
