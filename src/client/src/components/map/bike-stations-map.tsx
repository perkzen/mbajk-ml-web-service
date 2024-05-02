'use client';
import { useEffect, useState } from 'react';
import { APIProvider, Map as GoogleMap } from '@vis.gl/react-google-maps';
import StationMarker from '@/components/map/station-marker';
import { Drawer } from '@/components/ui/drawer';
import BikeStationInfoWindow from '@/components/map/info-window/bike-station-info-window';
import { useQueryParams } from '@/lib/hooks/use-querey-params';
import { useBikeStations } from '@/lib/hooks/bike-stations';
import BikeStationTabs from '@/components/map/bike-station-tabs';
import MapActions from '@/components/map/map-actions';


export const center = {
  lat: 46.5590,
  lng: 15.6381,
};

export const DEFAULT_ZOOM = 14;


const BikeStationsMap = () => {
  const { data: stations = [] } = useBikeStations();

  const { urlQuery, updateQueryParams, deleteQueryParams } = useQueryParams();
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = (stationNumber: number) => {
    updateQueryParams({ ...urlQuery, station: stationNumber });
    setIsOpen(true);
  };

  const handleClose = () => {
    deleteQueryParams('station');
    setIsOpen(false);
  };

  useEffect(() => {
    if (urlQuery.station) {
      setIsOpen(true);
    }
  }, [urlQuery.station]);

  return (
    <Drawer
      open={isOpen}
      dismissible={true}
      direction={'left'}
      modal={false}
      onRelease={(_, open) => {
        setIsOpen(open);
      }}
    >
      <APIProvider apiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY as string}>
        <GoogleMap
          defaultCenter={center}
          defaultZoom={DEFAULT_ZOOM}
          gestureHandling={'greedy'}
          disableDefaultUI={true}
          className={'w-full h-full flex-grow relative'}
          mapId={'google-map-id'}
        >
          <MapActions />
          <BikeStationTabs />
          {stations.map((station) => (
            <StationMarker
              key={station.number}
              lat={station.lat}
              lon={station.lon}
              number={station[urlQuery.show]}
              onClick={() => handleOpen(station.number)} />
          ))}
        </GoogleMap>
      </APIProvider>
      <BikeStationInfoWindow onClose={handleClose} />
    </Drawer>

  );
};

export default BikeStationsMap;