// Cache name for the application shell
const CACHE_NAME = 'flame-steward-v1';
// List of core files to cache (the application shell)
const urlsToCache = [
  'stewardship_console.html',
  'manifest.json',
  // Tailwind CDN URL is dynamic and often non-cacheable, relying on network for aesthetic,
  // but the core HTML/JS structure will load immediately.
];

// Installation event: caches the application shell
self.addEventListener('install', event => {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache and added core shell files');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activation event: clears old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event: serves assets from cache, falling back to network
self.addEventListener('fetch', event => {
  // Only intercept requests for the app shell, not API calls
  const url = new URL(event.request.url);

  // Do not intercept API calls (which always need fresh network data) or cross-origin requests
  if (url.origin === location.origin && urlsToCache.includes(url.pathname.substring(1))) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          // Cache hit - return response
          if (response) {
            return response;
          }
          // No cache hit - fetch from network
          return fetch(event.request);
        }
      )
    );
  }
});

