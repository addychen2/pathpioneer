import React, { useEffect } from 'react';
import { View } from 'react-native';
import Button from '../components/button';
import AddressInput from '../components/addressInput';
import HierarchyConatiner from '../components/hierarchyContainer';
import HeirarchyInput from '../components/setHierarchy';
import MultiAddressContainer from '../components/multiaddresscontainer';
import { sendAddress } from '../API';

export default function Prompt(){
    return(
        <View style="scrollable-con">
        <MultiAddressContainer/>
        <Button onPress={sendAddress} title="Submit"/>
        </View>
    );
}
