import { useEffect, useState } from 'react';

import { View, ActivityIndicator } from 'react-native';
import HomeStudentProfile from './homeStudentProfile';
import { styles } from '@/constants/styles';
import HomeSupervisorProfile from './homeSupervisorProfile';
import { getUserRole } from '@/api/getUserRole';

export default function HomeProfile() {
    const [userRole, setUserRole] = useState<'student' | 'supervisor' | null>(null);
    const [userId, setUserId] = useState<string | undefined>(undefined);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            const data = await getUserRole();
            if (!data) return;

            const { role: myRole, id: myId } = data;
            setUserRole(myRole);
            setUserId(myId);
            setLoading(false);
        };

        fetchUser();
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
