import { Drawer } from 'expo-router/drawer';
import { Ionicons } from '@expo/vector-icons';
import { styles } from '@/constants/styles';
import CustomDrawer from '@/components/custom_components/customDrawer';
import { firstColor, greenColor } from '@/constants/Colors';

export default function DrawerLayout() {
    return (
        <Drawer
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
                drawerLabelStyle: [{ marginLeft: 25 }, styles.drawerMenuTextStyle],
                drawerItemStyle: styles.drawerItemStyle,
                headerStyle: { backgroundColor: greenColor },
                headerTintColor: greenColor,
                headerTitleStyle: styles.headerTextStyle,
            })}
        >
            <Drawer.Screen name="homeStack" options={{ title: 'Strona główna' }} />
            <Drawer.Screen name="supervisorsListStack" options={{ title: 'Promotorzy' }} />
            <Drawer.Screen name="thesisesListStack" options={{ title: 'Prace dyplomowe' }} />
        </Drawer>
    );
}
