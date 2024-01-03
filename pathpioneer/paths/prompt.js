import React, { useEffect } from 'react';
import { View } from 'react-native';
import Button from '../components/button';
import AddressInput from '../components/addressInput';
import HierarchyConatiner from '../components/hierarchyContainer';
import MultiAddressContainer from '../components/multiaddresscontainer';

export default function Prompt(){
    return(
        <View>
        <MultiAddressContainer/>
        </View>
    );
}