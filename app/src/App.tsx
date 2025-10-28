import React from 'react';
import HazardMap from './features/hazards/HazardMap';
import WeatherCard from './features/weather/WeatherCard';

export default function App(): React.JSX.Element {
	return (
		<div className="min-h-screen bg-slate-900 text-slate-50">
			<div className="mx-auto max-w-5xl p-4">
				<h1 className="text-2xl font-semibold">澳門災情互助地圖</h1>
				<p className="text-slate-300 mt-2">
					MVP 初始化成功。接下來會加入地圖、災情標記、天氣與社交功能。
				</p>
				<div className="mt-6">
					<HazardMap />
				</div>
				<WeatherCard />
			</div>
		</div>
	);
}


