import React from 'react';
import MapView from 'react-native-maps';
import { StyleSheet, View } from 'react-native';
import { PROVIDER_GOOGLE } from 'react-native-maps';
import {Marker} from 'react-native-maps';
import { getRoute } from './API';
import { getLonLat } from './API';
import { getDistanceMatrix } from './API';


export default function App() {
  getDistanceMatrix()
  //getRoute()
  //getLonLat()
  return (
    <View style={styles.container}>
      <MapView style={styles.map} provider={PROVIDER_GOOGLE}>
      <Marker
        coordinate={{latitude: -34.397, longitude: 150.644}}
        title='bing bang'
        description='bingyee bangeee'
    />
  </MapView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
});
