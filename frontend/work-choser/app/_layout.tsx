import 'react-native-reanimated';
import { useState } from 'react';
import LoginView from '@/components/custom_components/loginView';

import { Slot } from 'expo-router';

export default function RootLayout() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    if (!isLoggedIn) {
        return <LoginView setIsLoggedIn={setIsLoggedIn} />;
    }

    return <Slot />;
}
