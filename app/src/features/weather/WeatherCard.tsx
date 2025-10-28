import React, { useEffect, useState } from 'react';
import { fetchWeather, type WeatherNow } from './openMeteo';

const macau: [number, number] = [22.1987, 113.5439];

export default function WeatherCard(): React.JSX.Element {
	const [data, setData] = useState<WeatherNow | null>(null);
	const [err, setErr] = useState<string | null>(null);

	useEffect(() => {
		fetchWeather(macau[0], macau[1]).then(setData).catch((e) => setErr(String(e)));
	}, []);

	return (
		<div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/40 p-4">
			<h2 className="font-medium">澳門即時天氣</h2>
			{err && <p className="text-red-400 text-sm mt-2">{err}</p>}
			{data ? (
				<div className="text-sm text-slate-300 mt-2 grid grid-cols-3 gap-4">
					<div>
						<p className="text-slate-400">氣溫</p>
						<p className="text-slate-50 text-lg">{data.temperature ?? '-'}°C</p>
					</div>
					<div>
						<p className="text-slate-400">風速</p>
						<p className="text-slate-50 text-lg">{data.windSpeed ?? '-'} m/s</p>
					</div>
					<div>
						<p className="text-slate-400">降水</p>
						<p className="text-slate-50 text-lg">{data.precipitation ?? '-'} mm</p>
					</div>
				</div>
			) : (
				<p className="text-slate-400 text-sm mt-2">載入中...</p>
			)}
			<p className="text-xs text-slate-500 mt-3">資料來源：Open-Meteo</p>
		</div>
	);
}


