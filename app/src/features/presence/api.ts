import { supabase, isSupabaseReady } from '@/lib/supabase';

export type PresenceRow = {
	device_id: string;
	updated_at: string;
	lat: number;
	lng: number;
};

export async function upsertPresence(lat: number, lng: number): Promise<void> {
	if (!isSupabaseReady) return;
	const device_id = ensureDeviceId();
	const { error } = await supabase.from('presence').upsert({ device_id, lat, lng, updated_at: new Date().toISOString() });
	if (error) throw error;
}

export async function listPresence(): Promise<PresenceRow[]> {
	if (!isSupabaseReady) return [];
	const { data, error } = await supabase
		.from('presence')
		.select('*')
		.order('updated_at', { ascending: false })
		.limit(200);
	if (error) throw error;
	return data ?? [];
}

export function subscribePresence(onUpsert: (row: PresenceRow) => void) {
	if (!isSupabaseReady) return { unsubscribe() {} } as any;
	return supabase
		.channel('presence-ch')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'presence' }, (payload) => onUpsert(payload.new as PresenceRow))
		.on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'presence' }, (payload) => onUpsert(payload.new as PresenceRow))
		.subscribe();
}

function ensureDeviceId(): string {
	const key = 'device_id';
	const existing = localStorage.getItem(key);
	if (existing) return existing;
	const id = crypto.randomUUID();
	localStorage.setItem(key, id);
	return id;
}
