import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';
// Leaflet CSS 由 index.html 的 CDN 載入，避免本機包丟失時無法解析

const container = document.getElementById('root');
if (!container) throw new Error('Root container not found');
createRoot(container).render(
	<React.StrictMode>
		<App />
	</React.StrictMode>
);


