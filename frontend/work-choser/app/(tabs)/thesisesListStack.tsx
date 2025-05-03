import { createNativeStackNavigator } from '@react-navigation/native-stack';
import ThesisesList from './thesisesList';
import ThesisDescription from './thesisDescription';

const Stack = createNativeStackNavigator();

export default function ThesisesListStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="ThesisesList"
                component={ThesisesList}
                options={{ title: 'Theses List', headerShown: false }}
            />
            <Stack.Screen
                name="ThesisDescription"
                component={ThesisDescription}
                options={{ title: 'Thesis Description' }}
            />
        </Stack.Navigator>
    );
}
