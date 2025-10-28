import React, { useEffect, useRef, useState } from 'react';
import { upsertPresence, listPresence, subscribePresence, type PresenceRow } from './api';
import L from 'leaflet';
import { Marker, Popup, useMap } from 'react-leaflet';

const blueIcon = new L.Icon({
	iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
	iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
	shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41],
});

export function PresenceMarkers(): React.JSX.Element | null {
	const map = useMap();
	const [rows, setRows] = useState<PresenceRow[]>([]);
	useEffect(() => {
		listPresence().then(setRows).catch(() => {});
		const sub = subscribePresence((row) => setRows((prev) => {
			const idx = prev.findIndex((r) => r.device_id === row.device_id);
			if (idx >= 0) {
				const copy = prev.slice();
				copy[idx] = row;
				return copy;
			}
			return [row, ...prev];
		}));
		return () => { try { sub.unsubscribe(); } catch {} };
	}, []);

	return (
		<>
			{rows.map((r) => (
				<Marker key={r.device_id} position={[r.lat, r.lng]} icon={blueIcon}>
					<Popup>
						<div className="text-sm">志願者位置<br />{r.lat.toFixed(5)}, {r.lng.toFixed(5)}</div>
					</Popup>
				</Marker>
			))}
		</>
	);
}

export default function PresenceToggle(): React.JSX.Element {
	const [enabled, setEnabled] = useState<boolean>(false);
	const watchId = useRef<number | null>(null);

	useEffect(() => {
		if (!enabled) {
			if (watchId.current !== null) {
				navigator.geolocation.clearWatch(watchId.current);
				watchId.current = null;
			}
			return;
		}
		if (!('geolocation' in navigator)) return;
		watchId.current = navigator.geolocation.watchPosition(
			(pos) => {
				upsertPresence(pos.coords.latitude, pos.coords.longitude).catch(() => {});
			},
			() => {},
			{ enableHighAccuracy: true, maximumAge: 5000 }
		);
		return () => {
			if (watchId.current !== null) {
				navigator.geolocation.clearWatch(watchId.current);
				watchId.current = null;
			}
		};
	}, [enabled]);

	return (
		<label className="inline-flex items-center gap-2 text-sm">
			<input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />
			<span>分享我的位置</span>
		</label>
	);
}
