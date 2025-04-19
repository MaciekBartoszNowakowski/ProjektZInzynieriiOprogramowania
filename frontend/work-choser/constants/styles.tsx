import { firstColor } from './Colors';
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    headerImage: {
        color: firstColor,
        bottom: -90,
        left: -35,
        position: 'absolute',
    },
    titleContainer: {
        flexDirection: 'row',
        gap: 8,
    },
    defaultImage: {
        alignSelf: 'center',
    },
    dafaultThemedText: {
        fontFamily: 'SpaceMono',
    },
});
