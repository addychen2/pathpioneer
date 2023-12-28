import React from 'react';
import MapView from 'react-native-maps';
import { StyleSheet, View } from 'react-native';
import { PROVIDER_GOOGLE } from 'react-native-maps';
import {Marker} from 'react-native-maps';
import { getRoute } from './API';
import { Polyline } from 'react-native-maps';


export default function App() {
  getRoute()
  return (
    <View style={styles.container}>
      <MapView style={styles.map} provider={PROVIDER_GOOGLE}>
      <Polyline
    coordinates={[
      {latitude: 37.8025259, longitude: -122.4351431},
      {latitude: 37.7896386, longitude: -122.421646},
      {latitude: 37.7665248, longitude: -122.4161628},
      {latitude: 37.7734153, longitude: -122.4577787},
      {latitude: 37.7948605, longitude: -122.4596065},
      {latitude: 37.8025259, longitude: -122.4351431},
    ]}
    strokeColor="#000" // fallback for when `strokeColors` is not supported by the map-provider
    strokeColors={[
      '#7F0000',
      '#00000000', // no color, creates a "long" gradient between the previous and next coordinate
      '#B24112',
      '#E5845C',
      '#238C23',
      '#7F0000',
    ]}
    strokeWidth={6}
  />
      <Marker
        coordinate={{latitude: 37.8025259, longitude: -122.4351431}}
        title='bing bang'
        description='bingyee bangeee'
    />
    <Marker
        coordinate={{latitude: 37.7896386, longitude: -122.421646}}
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
