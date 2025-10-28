import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
	plugins: [react()],
	server: {
		port: 5174,
		strictPort: true,
		host: true, // listen on all interfaces for LAN access
		open: false,
		hmr: { clientPort: 5174 },
	},
	preview: {
		port: 5173,
		strictPort: true,
		host: true, // expose preview server to LAN
	},
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url)),
		},
	},
	optimizeDeps: {
		include: ['react', 'react-dom', 'leaflet', 'react-leaflet'],
	},
	ssr: {
		noExternal: ['react-leaflet', 'leaflet'],
	},
});


