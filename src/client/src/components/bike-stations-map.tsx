'use client';
import { env } from '@/env.mjs';
import { memo } from 'react';
import { AdvancedMarker, APIProvider, Map as GoogleMap, Pin } from '@vis.gl/react-google-maps';

const containerStyle = {
  width: '100vw',
  height: '100vh',
};

const center = {
  lat: 46.5590,
  lng: 15.6381,
};


interface BikeStationsMapProps {
  stations: BikeStation[];
}

const BikeStationsMap = ({ stations = [] }: BikeStationsMapProps) => {
  return <APIProvider apiKey={env.NEXT_PUBLIC_GOOGLE_MAPS_KEY}>
    <GoogleMap
      defaultCenter={center}
      defaultZoom={14}
      gestureHandling={'greedy'}
      disableDefaultUI={true}
      style={containerStyle}
      mapId={'google-map-id'}
    >
      {stations.map((station) => (
        <AdvancedMarker
          key={station.number}
          position={{
            lat: station.lat,
            lng: station.lon,
          }}

        >
          <Pin background={'#fff'} borderColor={'#000'}>
            <div className="text-center font-bold bg-primary w-5 h-5 rounded-full text-white">
              <div className={'pt-1'}>{station.available_bikes}</div>
            </div>
          </Pin>
        </AdvancedMarker>
      ))}
    </GoogleMap>


  </APIProvider>;
};

export default memo(BikeStationsMap);