export const showMessage = (title: string, message: string) => {
    if (typeof window !== 'undefined') {
        window.alert(`${title}\n\n${message}`);
    }
};
