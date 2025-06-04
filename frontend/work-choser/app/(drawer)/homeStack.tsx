import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeProfile from '../panes/homeProfile';
import ThesisOwnerDescription from '../panes/thesisOwnerDescription';
import ThesisDescription from '../panes/thesisDescription';
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
        </Stack.Navigator>
    );
}
