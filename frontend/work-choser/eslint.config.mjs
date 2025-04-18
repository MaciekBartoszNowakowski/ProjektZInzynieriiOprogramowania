import js from '@eslint/js';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import parser from '@typescript-eslint/parser';
import pluginReact from 'eslint-plugin-react';
import pluginReactNative from 'eslint-plugin-react-native';
import pluginPrettier from 'eslint-plugin-prettier';
import { defineConfig } from 'eslint/config';

export default defineConfig([
    {
        files: ['**/*.{js,mjs,cjs,ts,jsx,tsx}'],
        languageOptions: {
            parser,
            ecmaVersion: 2021,
            sourceType: 'module',
            globals: {
                ...globals.node,
                __DEV__: true,
                ...globals.jest,
            },
        },
        plugins: {
            js,
            react: pluginReact,
            'react-native': pluginReactNative,
            prettier: pluginPrettier,
        },
        rules: {
            ...js.configs.recommended.rules,
            ...pluginReact.configs.flat.recommended.rules,
            ...tseslint.configs.recommended.rules,
            ...pluginPrettier.configs.recommended.rules,
            'prettier/prettier': 'warn',
            'react-native/no-inline-styles': 'warn',
            'react-native/no-color-literals': 'warn',
            'react/no-unescaped-entities': 'off',
            'react/react-in-jsx-scope': 'off',
        },
        settings: {
            react: {
                version: 'detect',
            },
        },
    },
]);
