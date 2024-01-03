import React from 'react';
import {SafeAreaView, StyleSheet, TextInput} from 'react-native';
import Button from './button';


const HeirarchyInput = () => {
     const [heirarchyNumber, onChangeHierachy] = React.useState('');
  
    return (
      <SafeAreaView>
        <TextInput
          style={styles.input}
          onChangeText={onChangeHierachy}
          value={heirarchyNumber}
          placeholder="Hierarchy"
          keyboardType="numeric"
        />
        <Button title = "Confirm" />
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
  
export default HeirarchyInput;