import React from 'react';
import {SafeAreaView, StyleSheet, TextInput} from 'react-native';
import Button from './button';

const AddressInput = () => {
  const [streetAddress, onChangeStreetAddress] = React.useState('');
  const [city, onChangeCity] = React.useState('');
  const [state, onChangeState] = React.useState('')
  const [number, onChangeNumber] = React.useState('');

  return (
    <SafeAreaView>
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
      <Button title = "save" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});

export default AddressInput;