import { useEffect, useState } from 'react';

import { View, ActivityIndicator } from 'react-native';
import HomeStudentProfile from '../panes/homeStudentProfile';
import { styles } from '@/constants/styles';
import HomeSupervisorProfile from '../panes/homeSupervisorProfile';

export default function HomeProfile() {
    const [userRole, setUserRole] = useState<'student' | 'supervisor' | null>(null);
    const [userId, setUserId] = useState<string | undefined>(undefined);
    const [loading, setLoading] = useState(true);

    const getUserRole = async () => {
        try {
            const response = await fetch('http://localhost:8000/users/me/', {
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });

            const data = await response.json();

            if (response.ok && data.user && data.user.role && data.user?.id) {
                setUserRole(data.user.role);
                setUserId(data.user.id);
            } else {
                console.error('empty role: ', data);
            }
        } catch (error) {
            console.error('Web error: ', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getUserRole();
    }, []);

    if (loading || userId === undefined) {
        return (
            <View style={styles.loadingStyle}>
                <ActivityIndicator size="large" />
            </View>
        );
    }

    if (userRole === 'student') {
        return <HomeStudentProfile id={userId} />;
    } else {
        return <HomeSupervisorProfile id={userId} />;
    }
}
