import 'react-native-reanimated';
import { useState } from 'react';
import LoginView from '@/app/panes/loginView';

import { Slot } from 'expo-router';

export default function RootLayout() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    if (!isLoggedIn) {
        return <LoginView setIsLoggedIn={setIsLoggedIn} />;
    }

    return <Slot />;
}
