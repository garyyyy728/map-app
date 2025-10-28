import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet.heat';

type Props = {
	points: Array<[number, number, number?]>; // [lat, lng, intensity]
};

export default function HeatLayer({ points }: Props): null {
	const map = useMap();
	useEffect(() => {
		const layer = (L as any).heatLayer(points as any, { radius: 22, blur: 18, maxZoom: 17 });
		layer.addTo(map);
		return () => {
			layer.remove();
		};
	}, [map, points]);
	return null;
}


