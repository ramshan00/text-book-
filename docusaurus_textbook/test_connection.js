const axios = require('axios');

async function testConnection(url) {
    console.log(`Testing ${url}...`);
    try {
        const response = await axios.post(url, { query: "Hello" });
        console.log(`SUCCESS: ${url} responded with:`, response.data);
    } catch (error) {
        if (error.response) {
            console.log(`FAILED: ${url} responded with status ${error.response.status}`);
            console.log('Data:', error.response.data);
        } else if (error.request) {
            console.log(`FAILED: ${url} - No response received (Timeout/Network Error).`);
            console.log(error.message);
        } else {
            console.log(`FAILED: ${url} - Error setting up request:`, error.message);
        }
    }
}

// Test both potential URLs
(async () => {
    await testConnection("https://ramsha00-bookrn.hf.space/ask");
    await testConnection("https://ramsha00-bookie.hf.space/ask");
})();
