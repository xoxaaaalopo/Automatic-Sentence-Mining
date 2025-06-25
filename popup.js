document. getElementById('generateSubs').addEventListener('click', async () => {
    // Get the active tab URL
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
    const videoUrl = tab.url;

    // Send the URL to your local server
    const response = await fetch('http://localhost:5001/generateSubs', {
        method:'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({url: videoUrl})
    });

    const data = await response.json();

    console.log('Server Response: ', data);
});