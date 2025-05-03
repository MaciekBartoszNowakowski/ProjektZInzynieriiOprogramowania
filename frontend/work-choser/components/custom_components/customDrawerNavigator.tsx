import * as SplashScreen from 'expo-splash-screen';
import 'react-native-reanimated';
import { createDrawerNavigator } from '@react-navigation/drawer';
import CustomDrawer from '@/components/custom_components/customDrawer';
import { Ionicons } from '@expo/vector-icons';
import { firstColor, greenColor } from '@/constants/Colors';
import { styles } from '@/constants/styles';
import StudentsProfile from '@/app/(tabs)/studentsProfile';
import ThesisesListStack from '@/app/(tabs)/thesisesListStack';
import SupervisorsListStack from '@/app/(tabs)/supervisorsListStack';

const Drawer = createDrawerNavigator();

SplashScreen.preventAutoHideAsync();

export default function CustomDrawerNavigator() {
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
            })}
        >
            <Drawer.Screen name="Student" component={StudentsProfile} />

            <Drawer.Screen name="Supervisors" component={SupervisorsListStack} />
            <Drawer.Screen name="Thesises List" component={ThesisesListStack} />
        </Drawer.Navigator>
    );
}
