import * as SplashScreen from 'expo-splash-screen';
import 'react-native-reanimated';
import CustomDrawerNavigator from '@/components/custom_components/customDrawerNavigator';
import { useState } from 'react';
import LoginView from '@/components/custom_components/loginView';

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    if (isLoggedIn === false) {
        return <LoginView setIsLoggedIn={setIsLoggedIn} />;
    } else {
        return <CustomDrawerNavigator />;
    }
}
