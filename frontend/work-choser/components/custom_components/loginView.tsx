import React, { useState } from 'react';
import { View, TextInput, Text, Button } from 'react-native';
import { styles } from '@/constants/styles';
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

    const sendLoginData = async () => {
        try {
            const response = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username: login, password: password }),
            });

            const data = await response.json();

            if (response.ok) {
                // const accessToken = data.access;
                // const refreshToken = data.refresh;
                // await storeTokens(accessToken, refreshToken);

                console.log('Sukces: ', data);
                setError(false);
            } else {
                console.error('serwer error: ', data);
                setError(true);
                console.log(error);
            }
        } catch (error) {
            console.error('Błąd sieci: ', error);
        }
    };

    const handleLogin = async () => {
        await sendLoginData();
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
