import AsyncStorage from '@react-native-async-storage/async-storage';

export const storeTokens = async (accessToken: string, refreshToken: string): Promise<void> => {
    try {
        await AsyncStorage.setItem('accessToken', accessToken);
        await AsyncStorage.setItem('refreshToken', refreshToken);
    } catch (e) {
        console.error('Błąd zapisu tokenów', e);
    }
};

export const getAccessToken = async (): Promise<string | null> => {
    try {
        const token = await AsyncStorage.getItem('accessToken');
        return token;
    } catch (e) {
        console.error('Błąd odczytu accessToken:', e);
        return null;
    }
};
