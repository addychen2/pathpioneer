import React, { useEffect, useState } from 'react';
import { Pressable, View } from 'react-native';
import Button from '../components/button';
import AddressInput from '../components/addressInput';
import { FlatList } from 'react-native';
import { StyleSheet } from 'react-native';
import { Text } from 'react-native';

const globalArray = [];
let nextId = 0;
export default function HierarchyConatiner(){
    const [addresses, setAddresses] = useState([]);

    const addAddress = () => {
        setAddresses( // Replace the state
            [ // with a new array
                ...addresses, // that contains all the old items
                { id: nextId++ } // and one new item at the end

            ]
        )
    }

    return (
        <View>
            <FlatList
                data={addresses}
                renderItem={({item}) => <AddressInput/>}
            />
            <Button onPress={addAddress} title="Add Address"/>
        </View>
        );
}

const styles = StyleSheet.create({
    button: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 12,
        paddingHorizontal: 32,
        borderRadius: 4,
        elevation: 3,
        backgroundColor: 'black',
      },
      text: {
        fontSize: 16,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
        color: 'white',
      },
  });

export {globalArray};