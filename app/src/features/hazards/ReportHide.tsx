import React, { useEffect, useState } from 'react';

function useHiddenIds() {
	const key = 'hidden_hazard_ids';
	const [ids, setIds] = useState<Set<string>>(new Set());
	useEffect(() => {
		const raw = localStorage.getItem(key);
		if (raw) setIds(new Set(JSON.parse(raw)));
	}, []);
	useEffect(() => {
		localStorage.setItem(key, JSON.stringify(Array.from(ids)));
	}, [ids]);
	return {
		ids,
		hide: (id: string) => setIds((prev) => new Set(prev).add(id)),
		unhide: (id: string) => setIds((prev) => { const s = new Set(prev); s.delete(id); return s; }),
	};
}

export function ReportButtons({ id, onHide }: { id: string; onHide: (id: string) => void }): React.JSX.Element {
	const { hide } = useHiddenIds();
	return (
		<div className="flex gap-2 text-xs mt-2">
			<button className="px-2 py-1 bg-slate-800 rounded" onClick={() => { alert('已收到檢舉，稍後審核'); }}>檢舉</button>
			<button className="px-2 py-1 bg-slate-800 rounded" onClick={() => { hide(id); onHide(id); }}>隱藏</button>
		</div>
	);
}

export function filterHidden<T extends { id: string }>(rows: T[]): T[] {
	const key = 'hidden_hazard_ids';
	const raw = localStorage.getItem(key);
	const hidden = new Set<string>(raw ? JSON.parse(raw) : []);
	return rows.filter((r) => !hidden.has(r.id));
}


