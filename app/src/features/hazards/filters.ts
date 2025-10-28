import { type HazardRow, type HazardType } from './api';

export type TimeWindow = 'all' | '1h' | '6h' | '24h' | '7d';

export function filterHazards(rows: HazardRow[], types: HazardType[], window: TimeWindow): HazardRow[] {
	const byType = rows.filter((r) => types.includes(r.type));
	if (window === 'all') return byType;
	const now = Date.now();
	const ms = window === '1h' ? 3600000 : window === '6h' ? 21600000 : window === '24h' ? 86400000 : 604800000;
	return byType.filter((r) => now - new Date(r.created_at).getTime() <= ms);
}


