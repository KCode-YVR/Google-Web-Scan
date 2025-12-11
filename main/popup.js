const scanButton = document.getElementById('scanButton');
const resultsDiv = document.getElementById('results');

async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

async function handleScanClick() {
    resultsDiv.innerHTML = "You pressed the button. Getting URLs...";
    const curTab = await getCurrentTab();
    const tabURL = curTab.url;
    resultsDiv.innerHTML += 'Current Tab URL is: ' + tabURL;
    console.log("Current URL:", tabURL);
}

scanButton.addEventListener('click', handleScanClick);

