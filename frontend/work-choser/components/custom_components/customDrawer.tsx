import React from 'react';
import { View, Text } from 'react-native';
import {
    DrawerContentComponentProps,
    DrawerContentScrollView,
    DrawerItemList,
} from '@react-navigation/drawer';
import { styles } from '@/constants/styles';

const CustomDrawer = (props: DrawerContentComponentProps) => {
    return (
        <View style={styles.mainCustomDrawerStyle}>
            <View style={styles.firstCustomDrawerStyle}>
                <Text style={styles.menuNameStyle}> Menu </Text>
            </View>

            <View style={styles.secondCustomDrawerStyle}>
                <DrawerContentScrollView {...props}>
                    <DrawerItemList {...props} />
                </DrawerContentScrollView>
            </View>
        </View>
    );
};

export default CustomDrawer;
