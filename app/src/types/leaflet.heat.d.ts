declare module 'leaflet.heat' {
  import * as L from 'leaflet';
  interface HeatLatLngTuple extends Array<number> {
    0: number; // lat
    1: number; // lng
    2?: number; // intensity
  }
  interface HeatMapOptions {
    minOpacity?: number;
    maxZoom?: number;
    max?: number;
    radius?: number;
    blur?: number;
    gradient?: { [key: number]: string };
  }
  export function heatLayer(latlngs?: HeatLatLngTuple[], options?: HeatMapOptions): L.Layer & {
    setLatLngs(latlngs: HeatLatLngTuple[]): this;
    addLatLng(latlng: HeatLatLngTuple): this;
  };
}
