import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // Served embedded inside Django under STATIC_URL, from an arbitrary
  // sub-path, so every built asset is referenced with an absolute
  // `/static/...` URL instead of a relative one.
  base: '/static/',
  build: {
    // Everything (index.html, favicon.ico from public/, and the
    // JS/CSS/asset bundles under assets/) is emitted here, matching
    // Django's STATIC_URL directory and `base: '/static/'` above.
    // Rollup's assetFileNames/outDir can't point outside outDir (no
    // leading `../`), so index.html is built here too and then moved
    // into the templates dir by the `postbuild` script in package.json.
    outDir: '../xii/django_river_admin/static',
    emptyOutDir: true
  },
  server: {
    proxy: {
      // Best-effort dev proxy: forwards every known backend API prefix
      // used by this app to the Django dev server. The frontend routes
      // itself live behind a `#` (hash history), so they never collide
      // with these real HTTP paths.
      '^/(user|workflow|workflows|state|states|function|permission|group|transition-meta|transition-approval-meta|transition-hook|approval-hook|transition-approval|transition|workflow-object|api-token-auth)(/|$)': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: [],
    include: ['tests/unit/**/*.spec.js'],
    // Vitest externalizes node_modules deps by default and hands them to
    // Node's native ESM loader, which can't process the raw `.css` side
    // imports that vuetify's component modules ship with. Force it
    // through Vite's transform pipeline instead so those CSS imports are
    // handled (and no-op'd) like everything else in jsdom.
    server: {
      deps: {
        inline: ['vuetify']
      }
    }
  }
})
