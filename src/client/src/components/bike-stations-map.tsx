'use client';
import { GoogleMap, Marker, MarkerF, useJsApiLoader } from '@react-google-maps/api';
import { env } from '@/env.mjs';
import { memo, useCallback, useState } from 'react';

const containerStyle = {
  width: '100vw',
  height: '100vh',
};

const center = {
  lat: 46.5590,
  lng: 15.6381,
};


const BikeStationsMap = () => {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: env.NEXT_PUBLIC_GOOGLE_MAPS_KEY,
  });


  const [map, setMap] = useState<google.maps.Map | null>(null);

  const onLoad = useCallback(function callback(map: google.maps.Map) {
    // This is just an example of getting and using the map instance!!! don't just blindly copy!
    const bounds = new window.google.maps.LatLngBounds(center);
    map.fitBounds(bounds);

    setMap(map);
  }, []);

  const onUnmount = useCallback(function callback(map: google.maps.Map) {
    setMap(null);
  }, []);

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      <MarkerF position={center} label={{
        color: 'white',
        text: '1',
      }} />

      <></>
    </GoogleMap>
  ) : <></>;
};

export default memo(BikeStationsMap);