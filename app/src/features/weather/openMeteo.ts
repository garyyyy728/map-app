export type WeatherNow = {
	temperature: number | null;
	windSpeed: number | null;
	precipitation: number | null;
};

export async function fetchWeather(lat: number, lng: number): Promise<WeatherNow> {
	const params = new URLSearchParams({
		latitude: String(lat),
		longitude: String(lng),
		current: 'temperature_2m,precipitation,wind_speed_10m',
		timezone: 'Asia/Hong_Kong',
	});
	const res = await fetch(`https://api.open-meteo.com/v1/forecast?${params.toString()}`);
	const json = await res.json();
	const c = json.current ?? {};
	return {
		temperature: typeof c.temperature_2m === 'number' ? c.temperature_2m : null,
		windSpeed: typeof c.wind_speed_10m === 'number' ? c.wind_speed_10m : null,
		precipitation: typeof c.precipitation === 'number' ? c.precipitation : null,
	};
}


