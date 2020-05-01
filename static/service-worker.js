var CACHE_NAME = 'offline-calculator';
var urlsToCache = [
  '/static/css/bootstrap-iso.css',
  '/static/css/order_history_style.css',
  '/static/css/profile_style.css',
  '/static/css/responsive.css',
  '/static/css/style.css',
  '/static/css/stylesheet.css',
  '/static/javascript/common.js',
  '/static/javascript/DioProgress.js',
  '/static/javascript/global.js',
  '/static/javascript/jstree.min.js',
  '/static/javascript/query-2.1.1.min.js',
  '/static/javascript/lazysizes.min.js',
  '/static/javascript/main.js',
  '/static/javascript/parally.js',
  '/static/javascript/template.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'
];
self.addEventListener('install', function(event) {
  // install files needed offline
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// self.addEventListener('fetch', function(event) {
//   console.log(event.request.url);
//   event.respondWith(
//     caches.match(event.request).then(function(response) {
//       return response || fetch(event.request);
//     })
//   );
//  });

 self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request);
    })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          // Return true if you want to remove this cache,
          // but remember that caches are shared across
          // the whole origin
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});