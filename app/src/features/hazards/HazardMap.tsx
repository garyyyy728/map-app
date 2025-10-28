import React, { useEffect, useMemo, useState, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { createHazard, listHazards, subscribeHazards, type HazardRow, type HazardType } from './api';
import { filterHazards, type TimeWindow } from './filters';
import { filterHidden, ReportButtons } from './ReportHide';
import HeatLayer from './HeatLayer';
import PresenceToggle, { PresenceMarkers } from '../presence/PresenceToggle';

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

function ensureDeviceId(): string {
	const key = 'device_id';
	const existing = localStorage.getItem(key);
	if (existing) return existing;
	const id = crypto.randomUUID();
	localStorage.setItem(key, id);
	return id;
}

function ClickAdd({ onAdd }: { onAdd: (lat: number, lng: number) => void }): null {
	useMapEvents({ click: (e: L.LeafletMouseEvent) => onAdd(e.latlng.lat, e.latlng.lng) });
	return null;
}

export default function HazardMap(): React.JSX.Element {
	const [hazards, setHazards] = useState<HazardRow[]>([]);
	const [addMode, setAddMode] = useState<boolean>(false);
	const [pendingType, setPendingType] = useState<'flood' | 'fire' | 'landslide' | 'other'>('flood');
	const [selectedTypes, setSelectedTypes] = useState<HazardType[]>(['flood','fire','landslide','other']);
	const [timeWindow, setTimeWindow] = useState<TimeWindow>('24h');
	const [showHeat, setShowHeat] = useState<boolean>(false);
	const [pendingNote, setPendingNote] = useState<string>('');
	const [lastError, setLastError] = useState<string | null>(null);

	useEffect(() => {
		listHazards().then(setHazards).catch((e) => console.error(e));
		const sub = subscribeHazards((row) => setHazards((prev) => [row, ...prev]));
		return () => {
			try { sub.unsubscribe(); } catch {}
		};
	}, []);

	const tiles = useMemo(
		() => (
			<TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
		),
		[]
	);

	const filtered = filterHidden(filterHazards(hazards, selectedTypes, timeWindow));
	const heatPoints = filtered.map((h) => [h.lat, h.lng, 0.6] as [number, number, number]);

	const handleAdd = useCallback(async (lat: number, lng: number) => {
		setLastError(null);
		// optimistic add (temporary id) for immediate feedback
		const temp: HazardRow = {
			id: `temp-${crypto.randomUUID()}`,
			created_at: new Date().toISOString(),
			lat,
			lng,
			type: pendingType,
			note: pendingNote || null,
			device_id: 'local',
		};
		setHazards((prev) => [temp, ...prev]);
		try {
			const device_id = ensureDeviceId();
			const row = await createHazard({ lat, lng, type: pendingType, note: pendingNote || null, device_id });
			setHazards((prev) => [row, ...prev.filter((h) => h.id !== temp.id)]);
		} catch (e: any) {
			console.error('Create hazard failed', e);
			setLastError('新增失敗: ' + (e?.message || '未知錯誤'));
			// rollback optimistic temp marker
			setHazards((prev) => prev.filter((h) => h.id !== temp.id));
		}
	}, [pendingType, pendingNote]);

	return (
		<div className="rounded-lg overflow-hidden border border-slate-800">
			<div className="flex flex-wrap items-center gap-2 p-3 bg-slate-900/50 border-b border-slate-800">
				<button
					className={`px-3 py-1.5 rounded text-sm ${addMode ? 'bg-sky-600 text-white' : 'bg-slate-800 text-slate-200'}`}
					onClick={() => setAddMode((v) => !v)}
				>
					{addMode ? '正在新增' : '新增模式'}
				</button>
				<select
					className="bg-slate-800 text-slate-100 text-sm px-2 py-1 rounded"
					value={pendingType}
					onChange={(e) => setPendingType(e.target.value as any)}
				>
					<option value="flood">水浸</option>
					<option value="fire">火災</option>
					<option value="landslide">山泥傾瀉</option>
					<option value="other">其他</option>
				</select>
				<input
					type="text"
					placeholder="備註（可留空）"
					className="flex-1 bg-slate-800 text-slate-100 text-sm px-3 py-1.5 rounded outline-none"
					value={pendingNote}
					onChange={(e) => setPendingNote(e.target.value)}
				/>
				<div className="w-px h-6 bg-slate-800" />
				<div className="flex items-center gap-2 text-sm">
					<label className="inline-flex items-center gap-1"><input type="checkbox" checked={selectedTypes.includes('flood')} onChange={(e) => setSelectedTypes((prev) => e.target.checked ? [...prev, 'flood'] : prev.filter(t => t !== 'flood'))} />水浸</label>
					<label className="inline-flex items-center gap-1"><input type="checkbox" checked={selectedTypes.includes('fire')} onChange={(e) => setSelectedTypes((prev) => e.target.checked ? [...prev, 'fire'] : prev.filter(t => t !== 'fire'))} />火災</label>
					<label className="inline-flex items-center gap-1"><input type="checkbox" checked={selectedTypes.includes('landslide')} onChange={(e) => setSelectedTypes((prev) => e.target.checked ? [...prev, 'landslide'] : prev.filter(t => t !== 'landslide'))} />山泥</label>
					<label className="inline-flex items-center gap-1"><input type="checkbox" checked={selectedTypes.includes('other')} onChange={(e) => setSelectedTypes((prev) => e.target.checked ? [...prev, 'other'] : prev.filter(t => t !== 'other'))} />其他</label>
				</div>
				<select className="bg-slate-800 text-slate-100 text-sm px-2 py-1 rounded" value={timeWindow} onChange={(e) => setTimeWindow(e.target.value as TimeWindow)}>
					<option value="1h">近1小時</option>
					<option value="6h">近6小時</option>
					<option value="24h">近24小時</option>
					<option value="7d">近7天</option>
					<option value="all">全部</option>
				</select>
				<label className="inline-flex items-center gap-2 text-sm ml-auto">
					<input type="checkbox" checked={showHeat} onChange={(e) => setShowHeat(e.target.checked)} />
					<span>熱度</span>
				</label>
				<div className="w-px h-6 bg-slate-800" />
				<PresenceToggle />
			</div>
			{lastError && (
				<p className="w-full text-sm text-red-400 -mt-1">{lastError}</p>
			)}
			<div className="h-[70vh] relative">
				{addMode && (
					<div className="pointer-events-none absolute top-2 left-1/2 -translate-x-1/2 z-[500] bg-sky-600/90 text-white text-xs px-3 py-1 rounded shadow">
						點擊地圖以新增：{pendingType === 'flood' ? '水浸' : pendingType === 'fire' ? '火災' : pendingType === 'landslide' ? '山泥傾瀉' : '其他'}
					</div>
				)}
				<MapContainer center={macauCenter} zoom={13} style={{ height: '100%', width: '100%', cursor: addMode ? 'crosshair' : 'grab' }}>
					{tiles}
					{addMode && (
						<ClickAdd onAdd={handleAdd} />
					)}
					{!showHeat && filtered.map((h) => (
						<Marker key={h.id} position={[h.lat, h.lng]} icon={defaultIcon}>
							<Popup>
								<div className="text-sm">
									<p className="font-medium">{
										h.type === 'flood' ? '水浸' : h.type === 'fire' ? '火災' : h.type === 'landslide' ? '山泥傾瀉' : '其他'
									}</p>
									<p className="text-slate-500">{h.lat.toFixed(5)}, {h.lng.toFixed(5)}</p>
									{h.note && <p className="mt-1">{h.note}</p>}
									<ReportButtons id={h.id} onHide={(id) => setHazards((prev) => prev.filter((x) => x.id !== id))} />
								</div>
							</Popup>
						</Marker>
					))}
					{showHeat && <HeatLayer points={heatPoints} />}
					<PresenceMarkers />
				</MapContainer>
			</div>
		</div>
	);
}


