import React, { useState } from 'react';
import { View, TextInput, Text, Button } from 'react-native';
import { styles } from '@/constants/styles';

type LoginViewProps = {
    // eslint-disable-next-line no-unused-vars
    setIsLoggedIn: (val: boolean) => void;
};

const LoginView = ({ setIsLoggedIn }: LoginViewProps) => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = () => {
        if (login === 'admin' && password === '1234') {
            setIsLoggedIn(true);
            setError('');
        } else {
            setIsLoggedIn(false);
            setError('Nieprawidłowy login lub hasło');
        }
    };

    return (
        <View style={styles.loginContainer}>
            <Text style={styles.loginLabel}>Login:</Text>
            <TextInput
                style={styles.loginInput}
                value={login}
                onChangeText={setLogin}
                placeholder="Wprowadź login"
                autoCapitalize="none"
            />

            <Text style={styles.loginLabel}>Hasło:</Text>
            <TextInput
                style={styles.loginInput}
                value={password}
                onChangeText={setPassword}
                placeholder="Wprowadź hasło"
                secureTextEntry={true}
            />

            <View style={styles.loginButtonContainer}>
                <Button title="Zaloguj się" onPress={handleLogin} />
            </View>

            {error ? <Text style={styles.loginError}>{error}</Text> : null}
        </View>
    );
};

export default LoginView;
