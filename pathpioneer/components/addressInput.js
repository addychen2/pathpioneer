import React from 'react';
import {SafeAreaView, StyleSheet, TextInput} from 'react-native';
import Button from './button';
import { globalArray } from './hierarchyContainer';

const AddressInput = (props) => {
  const [streetAddress, onChangeStreetAddress] = React.useState('');
  const [city, onChangeCity] = React.useState('');
  const [state, onChangeState] = React.useState('')
  const [number, onChangeNumber] = React.useState('');

  const addToArray = () => {
    globalArray[props.hierarchy].push(streetAddress + ", " + city + ", " + state + ", " + number);
  }
 
  console.log(globalArray);

  return (
    <SafeAreaView style={styles.container}>
      <TextInput
        style={styles.input}
        onChangeText={onChangeStreetAddress}
        placeholder="Street Address"
        value={streetAddress}
      />
      <TextInput
        style={styles.input}
        onChangeText={onChangeCity}
        placeholder="City"
        value={city}
      />
      <TextInput
        style={styles.input}
        onChangeText={onChangeState}
        placeholder="State"
        value={state}
      />
      <TextInput
        style={styles.input}
        onChangeText={onChangeNumber}
        value={number}
        placeholder="Zipcode"
        keyboardType="numeric"
      />
      <Button onPress={addToArray} title="save"/>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  /*
  container:{
    height: 50,
    width: 100,
    borderWidth: 1,
    
  },
  */
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});

export default AddressInput;