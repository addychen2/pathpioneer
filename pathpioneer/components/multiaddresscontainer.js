import React, { useState } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import HierarchyConatiner from './hierarchyContainer'; // Import the MultiAddressInput component

let nextId = 0;

export function MultiAddressContainer() {
    const [containers, setContainers] = useState([{ id: nextId++ }]);

    const addContainer = () => {
        setContainers([...containers, { id: nextId++ }]);
    }

    return (
        <View style={styles.container}>
            {containers.map(container => (
                <View key={container.id} style={styles.addressContainer}>
                    <HierarchyConatiner/>
                </View>
            ))}
            <Button onPress={addContainer} title="Add Container" />
        </View>
    );
}

const styles = StyleSheet.create({
    addressContainer: {
        borderWidth: 1,
        borderColor: 'black',
        borderRadius: 5,
        padding: 10,
        marginBottom: 10,
    },
});

export default MultiAddressContainer;