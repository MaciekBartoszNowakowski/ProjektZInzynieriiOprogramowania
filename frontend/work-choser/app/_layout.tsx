import * as SplashScreen from 'expo-splash-screen';
import 'react-native-reanimated';
import { createDrawerNavigator } from '@react-navigation/drawer';
import CustomDrawer from '@/components/custom_components/customDrawer';
import { Ionicons } from '@expo/vector-icons';
import { firstColor, greenColor } from '@/constants/Colors';
import { styles } from '@/constants/styles';
import StudentsProfile from './(tabs)/studentsProfile';
import SupervisorProfile from './(tabs)/supervisorProfile';
import SupervisorList from './(tabs)/supervisorsList';
import ThesisesList from './(tabs)/thesisesList';
const Drawer = createDrawerNavigator();

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
    return (
        <Drawer.Navigator
            drawerContent={(props) => <CustomDrawer {...props} />}
            screenOptions={({ navigation }) => ({
                headerLeft: () => (
                    <Ionicons
                        name="menu"
                        size={24}
                        color={firstColor}
                        style={styles.drawerHeader}
                        onPress={() => navigation.openDrawer()}
                    />
                ),
                drawerLabelStyle: [
                    {
                        marginLeft: 25,
                    },
                    styles.drawerMenuTextStyle,
                ],
                drawerItemStyle: styles.drawerItemStyle,
                headerStyle: {
                    backgroundColor: greenColor,
                },
                headerTintColor: greenColor,
                headerTitleStyle: styles.headerTextStyle,
                drawerActiveBackgroundColor: 'white',
                drawerActiveTintColor: 'chosenTextColor',
            })}
        >
            <Drawer.Screen name="Student" component={StudentsProfile} />
            <Drawer.Screen name="Supervisor Profile" component={SupervisorProfile} />
            <Drawer.Screen name="Supervisors List" component={SupervisorList} />
            <Drawer.Screen name="Thesises List" component={ThesisesList} />
        </Drawer.Navigator>
    );
}
