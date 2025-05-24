import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeProfile from '../panes/homeProfile';
import ThesisOwnerDescription from '../panes/thesisOwnerDescription';

const Stack = createNativeStackNavigator();

export default function HomeStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="HomeProfile"
                component={HomeProfile}
                options={{ title: 'HomeProfile' }}
            />
            <Stack.Screen
                name="ThesisOwnerDescription"
                component={ThesisOwnerDescription}
                options={{ title: 'Thesis Description' }}
            />
        </Stack.Navigator>
    );
}
