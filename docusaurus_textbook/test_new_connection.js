const axios = require('axios');

async function testConnection(url) {
    console.log(`Testing ${url}...`);
    try {
        const response = await axios.post(url, { query: "What is ROS2?" });
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

// Test the new user-provided URL
(async () => {
    await testConnection("https://ramsha00-bookramshy.hf.space/ask");
})();
