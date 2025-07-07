const CACHE_NAME = "secretbox-cache-v1";
const urlsToCache = ["/", "/offline"];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        fetch(event.request).catch(() =>
            caches.match(event.request).then(response => response || caches.match("/offline"))
        )
    );
});
