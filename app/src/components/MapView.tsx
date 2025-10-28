import React, { useMemo, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const macauCenter: [number, number] = [22.1987, 113.5439];

const defaultIcon = new L.Icon({
	iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
	iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
	shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41],
});

type Hazard = {
	id: string;
	lat: number;
	lng: number;
	type: 'flood' | 'fire' | 'other';
	note?: string;
};

function ClickToAdd({ onAdd }: { onAdd: (lat: number, lng: number) => void }): null {
	useMapEvents({
		click(e: L.LeafletMouseEvent) {
			onAdd(e.latlng.lat, e.latlng.lng);
		},
	});
	return null;
}

export default function MapView(): React.JSX.Element {
	const [hazards, setHazards] = useState<Hazard[]>([]);

	const mapTiles = useMemo(
		() => (
			<TileLayer
				attribution='&copy; OpenStreetMap contributors'
				url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			/>
		),
		[]
	);

	return (
		<div className="h-[70vh] rounded-lg overflow-hidden border border-slate-800">
			<MapContainer center={macauCenter} zoom={13} style={{ height: '100%', width: '100%' }}>
				{mapTiles}
				<ClickToAdd
					onAdd={(lat, lng) =>
						setHazards((prev) => [
							...prev,
							{ id: crypto.randomUUID(), lat, lng, type: 'flood' },
						])
					}
				/>
				{hazards.map((h) => (
					<Marker key={h.id} position={[h.lat, h.lng]} icon={defaultIcon}>
						<Popup>
							<div className="text-sm">
								<p className="font-medium">{h.type === 'flood' ? '水浸' : h.type}</p>
								<p className="text-slate-500">{h.lat.toFixed(5)}, {h.lng.toFixed(5)}</p>
							</div>
						</Popup>
					</Marker>
				))}
			</MapContainer>
		</div>
	);
}


