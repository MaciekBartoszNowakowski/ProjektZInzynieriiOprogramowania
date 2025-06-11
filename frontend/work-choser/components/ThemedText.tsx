import { Text, type TextProps, StyleSheet } from 'react-native';

import { useThemeColor } from '@/hooks/useThemeColor';
import { primaryBlue } from '@/constants/Colors';
export type ThemedTextProps = TextProps & {
    lightColor?: string;
    darkColor?: string;
    type?: 'default' | 'title' | 'defaultSemiBold' | 'subtitle' | 'link';
};

export function ThemedText({
    style,
    lightColor,
    darkColor,
    type = 'default',
    ...rest
}: ThemedTextProps) {
    const color = useThemeColor({ light: lightColor, dark: darkColor }, 'text');

    return (
        <Text
            style={[
                { color },
                type === 'default' ? styles.default : undefined,
                type === 'title' ? styles.title : undefined,
                type === 'defaultSemiBold' ? styles.defaultSemiBold : undefined,
                type === 'subtitle' ? styles.subtitle : undefined,
                type === 'link' ? styles.link : undefined,
                style,
            ]}
            {...rest}
        />
    );
}

const styles = StyleSheet.create({
    default: {
        fontSize: 20,
        lineHeight: 24,
    },
    defaultSemiBold: {
        fontSize: 20,
        lineHeight: 24,
        fontWeight: '600',
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        lineHeight: 32,
    },
    subtitle: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    link: {
        lineHeight: 30,
        fontSize: 20,
        color: primaryBlue,
    },
});
