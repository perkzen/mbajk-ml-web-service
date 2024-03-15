export interface BikeStation {
  available_bikes: number;
  available_bike_stands: number;
  name: string;
  address: string;
  number: number;
  lat: number;
  lon: number;
  last_updated: number;
}


export interface BikeStationPrediction {
  available_bike_stands: number;
  date: string;
}