/**
 * MEDICARE — GLOBAL CONFIGURATION
 */
(function() {
    if (window.MEDICARE_API_URL) return;

    const isLocal = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1' || 
                    window.location.hostname.includes('192.168.');

    if (isLocal) {
        window.MEDICARE_API_URL = 'http://localhost:8000';
    } else {
        // PRODUCTION URL (Render)
        window.MEDICARE_API_URL = 'https://medicare-api-xyyl.onrender.com'; // User will deploy to Render
    }
    console.log(`MediCare API Target: ${window.MEDICARE_API_URL}`);
})();
