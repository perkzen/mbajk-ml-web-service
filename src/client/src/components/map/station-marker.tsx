import { AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import { BikeStation } from '@/lib/models';


interface StationMarkerProps {
  station: BikeStation;
  onClick?: () => void;
}

const StationMarker = ({ station, onClick }: StationMarkerProps) => {
  return (
    <AdvancedMarker
      key={station.number}
      position={{
        lat: station.lat,
        lng: station.lon,
      }}
      onClick={onClick}
    >
      <Pin background={'#fff'} borderColor={'#000'}>
        <div className="text-center font-bold bg-primary w-5 h-5 rounded-full text-white">
          <div className={'pt-1'}>{station.available_bikes}</div>
        </div>
      </Pin>
    </AdvancedMarker>
  );
};

export default StationMarker;