import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ThesisesList from '../panes/thesisesList';
import ThesisDescription from '../panes/thesisDescription';

const Stack = createNativeStackNavigator();

export default function ThesisesListStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="ThesisesList"
                component={ThesisesList}
                options={{ title: 'Lista prac dyplomowych', headerShown: false }}
            />
            <Stack.Screen
                name="ThesisDescription"
                component={ThesisDescription}
                options={{ title: 'Opis pracy dyplomowej' }}
            />
        </Stack.Navigator>
    );
}
