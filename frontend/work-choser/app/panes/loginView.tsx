import React, { useState } from 'react';
import { View, TextInput, Text, Button } from 'react-native';
import { styles } from '@/constants/styles';
import { sendLoginData } from '@/api/sendLoginData';
// import { storeTokens } from './storageService';

type LoginViewProps = {
    // eslint-disable-next-line no-unused-vars
    setIsLoggedIn: (val: boolean) => void;
};

const LoginView = ({ setIsLoggedIn }: LoginViewProps) => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);
    // password Current1

    const handleLogin = async () => {
        const isError = await sendLoginData(login, password);
        setError(isError ?? true);
        if (!error) {
            setIsLoggedIn(true);
        }
    };

    return (
        <View style={styles.loginContainer}>
            <Text style={styles.loginLabel}>Login:</Text>
            <TextInput
                style={styles.loginInput}
                value={login}
                onChangeText={setLogin}
                placeholder="username"
                autoCapitalize="none"
            />

            <Text style={styles.loginLabel}>Hasło:</Text>
            <TextInput
                style={styles.loginInput}
                value={password}
                onChangeText={setPassword}
                placeholder="password"
                secureTextEntry={true}
            />

            <View style={styles.loginButtonContainer}>
                <Button title="login" onPress={handleLogin} />
            </View>

            {error ? <Text style={styles.loginError}>Login or Password is wrong</Text> : null}
        </View>
    );
};

export default LoginView;
