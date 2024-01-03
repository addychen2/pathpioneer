import React, { useState } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import HierarchyConatiner from './hierarchyContainer'; // Import the MultiAddressInput component
import { globalArray } from './hierarchyContainer';
import { ScrollView } from 'react-native';
let nextId = 0;

export function MultiAddressContainer() {
    const [containers, setContainers] = useState([]);

    const addContainer = () => {
        setContainers([...containers, { id: nextId++ }]);
        globalArray.push([]);
    }

    return (
        <ScrollView style={styles.container}>
            {containers.map(container => (
                <View key={container.id} style={styles.addressContainer}>
                    <HierarchyConatiner hierarchy={container.id}/>
                </View>
            ))}
            <Button onPress={addContainer} title="Add Hierarchy" />
        </ScrollView>
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