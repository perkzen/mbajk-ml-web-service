import { AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import { BikeStation } from '@/lib/models';


interface StationMarkerProps {
  lat: number;
  lon: number;
  number: number;
  onClick?: () => void;
}

const StationMarker = ({ lat, lon, number, onClick }: StationMarkerProps) => {
  return (
    <AdvancedMarker
      position={{
        lat: lat,
        lng: lon,
      }}
      onClick={onClick}
    >
      <Pin background={'#fff'} borderColor={'#000'}>
        <div className="text-center font-bold bg-primary w-5 h-5 rounded-full text-white">
          <div className={'pt-1'}>{number}</div>
        </div>
      </Pin>
    </AdvancedMarker>
  );
};

export default StationMarker;