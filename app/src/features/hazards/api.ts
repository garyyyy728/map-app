import { supabase, isSupabaseReady } from '@/lib/supabase';

export type HazardType = 'flood' | 'fire' | 'landslide' | 'other';

export type HazardRow = {
	id: string;
	created_at: string;
	lat: number;
	lng: number;
	type: HazardType;
	note: string | null;
	device_id: string;
};

export async function listHazards(): Promise<HazardRow[]> {
	if (!isSupabaseReady) return [];
	const { data, error } = await supabase
		.from('hazards')
		.select('*')
		.order('created_at', { ascending: false })
		.limit(500);
	if (error) throw error;
	return data ?? [];
}

export async function createHazard(input: Omit<HazardRow, 'id' | 'created_at'>): Promise<HazardRow> {
	if (!isSupabaseReady) {
		return {
			id: crypto.randomUUID(),
			created_at: new Date().toISOString(),
			...input,
		};
	}
	const { data, error } = await supabase.from('hazards').insert(input).select('*').single();
	if (error) throw error;
	return data as HazardRow;
}

export function subscribeHazards(onInsert: (row: HazardRow) => void) {
	if (!isSupabaseReady) return { unsubscribe() {} } as any;
	return supabase
		.channel('hazards-ch')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'hazards' }, (payload) => {
			onInsert(payload.new as HazardRow);
		})
		.subscribe();
}


