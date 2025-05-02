import React from 'react';
import { View, Text } from 'react-native';
import {
    DrawerContentComponentProps,
    DrawerContentScrollView,
    DrawerItem,
} from '@react-navigation/drawer';
import { styles } from '@/constants/styles';

const CustomDrawer = (props: DrawerContentComponentProps) => {
    const { state, navigation, descriptors } = props;
    const activeRoute = state.routeNames[state.index];

    return (
        <View style={styles.mainCustomDrawerStyle}>
            <View style={styles.firstCustomDrawerStyle}>
                <Text style={styles.menuNameStyle}> Menu </Text>
            </View>

            <View style={styles.secondCustomDrawerStyle}>
                <DrawerContentScrollView>
                    {state.routes.map((route) => {
                        const isFocused = route.name === activeRoute;
                        const label =
                            descriptors[route.key]?.options.drawerLabel ??
                            descriptors[route.key]?.options.title ??
                            route.name;

                        return (
                            <DrawerItem
                                key={route.key}
                                label={label}
                                focused={isFocused}
                                onPress={() => navigation.navigate(route.name)}
                                labelStyle={
                                    isFocused ? styles.activeLabelStyle : styles.inactiveLabelStyle
                                }
                                style={
                                    isFocused ? styles.activeItemStyle : styles.inactiveItemStyle
                                }
                            />
                        );
                    })}
                </DrawerContentScrollView>
            </View>
        </View>
    );
};

export default CustomDrawer;
