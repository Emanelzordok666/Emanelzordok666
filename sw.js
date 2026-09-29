// Clause & Effect: always serves the newest game when online, and keeps a copy for offline play.
const CACHE = 'clause-effect-v7';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(CORE.map(u => fetch(u, { cache: 'no-store' }).then(r => r.ok && c.put(u, r)).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;
  const fonts = /^fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!sameOrigin && !fonts) return;
  const page = req.mode === 'navigate' || (sameOrigin && /\/(index\.html)?$/.test(url.pathname));
  const net = page ? fetch(req, { cache: 'no-store' }) : fetch(req);
  e.respondWith(
    net.then(res => {
      if (res && (res.ok || res.type === 'opaque')) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(page ? './index.html' : req, copy)); }
      return res;
    }).catch(() => caches.match(page ? './index.html' : req, { ignoreSearch: true }).then(hit => hit || caches.match(req, { ignoreSearch: true })))
  );
});
