import { createClient } from '@supabase/supabase-js';

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const anon = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

export const isSupabaseReady = Boolean(url && anon);
if (!isSupabaseReady) {
	// eslint-disable-next-line no-console
	console.warn('Supabase env not set. Add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY');
}

export const supabase = isSupabaseReady
	? createClient(url!, anon!)
	: ({} as ReturnType<typeof createClient>);


