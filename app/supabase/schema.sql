-- Hazards table for user-contributed disaster reports
create table if not exists public.hazards (
	id uuid primary key default gen_random_uuid(),
	created_at timestamptz not null default now(),
	lat double precision not null,
	lng double precision not null,
	type text not null check (type in ('flood','fire','landslide','other')),
	note text,
	device_id uuid not null
);

-- Simple presence table for optional live location (anonymized by device)
create table if not exists public.presence (
	device_id uuid primary key,
	updated_at timestamptz not null default now(),
	lat double precision not null,
	lng double precision not null
);

-- Row Level Security
alter table public.hazards enable row level security;
alter table public.presence enable row level security;

-- Public can read hazards and presence
create policy "hazards_read" on public.hazards for select using (true);
create policy "presence_read" on public.presence for select using (true);

-- Anyone can insert hazards (unauthenticated), limit payload size by constraints only
create policy "hazards_insert" on public.hazards for insert with check (true);

-- Allow delete own hazards by matching device_id via JWT if provided; else deny
create policy "hazards_delete_own" on public.hazards for delete using (
	auth.jwt() ?->> 'device_id' = device_id::text
);

-- Upsert presence for device
create policy "presence_upsert" on public.presence for insert with check (true);
create policy "presence_update" on public.presence for update using (
	auth.jwt() ?->> 'device_id' = device_id::text
) with check (
	auth.jwt() ?->> 'device_id' = device_id::text
);

-- Helpful indexes
create index if not exists hazards_created_at_idx on public.hazards (created_at desc);
create index if not exists hazards_location_idx on public.hazards using gist (
	-- approximate geospatial index with point
	( point(lng, lat) )
);


