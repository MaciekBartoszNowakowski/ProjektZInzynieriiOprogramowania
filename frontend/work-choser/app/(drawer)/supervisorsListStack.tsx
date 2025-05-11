import { createNativeStackNavigator } from '@react-navigation/native-stack';
import SupervisorList from '../panes/supervisorsList';
import SupervisorProfile from '../panes/supervisorProfile';
import ThesisDescription from '../panes/thesisDescription';

const Stack = createNativeStackNavigator();

export default function SupervisorsListStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen
                name="SupervisorsList"
                component={SupervisorList}
                options={{ title: 'Supervisors List' }}
            />
            <Stack.Screen
                name="SupervisorProfile"
                component={SupervisorProfile}
                options={{ title: 'Supervisor Profile' }}
            />
            <Stack.Screen
                name="ThesisDescription"
                component={ThesisDescription}
                options={{ title: 'Thesis Description' }}
            />
        </Stack.Navigator>
    );
}
