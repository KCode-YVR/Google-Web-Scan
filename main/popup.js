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
     if (!curTab || !curTab.url) {
        resultsDiv.innerHTML += 'Unable to read the current tab url.';
        return;
    }
    const tabURL = curTab.url;
    const tabDomain = extractDomain(curTab.url);
    resultsDiv.innerHTML += 'Current Tab URL is: ' + tabURL + '. Its domain name is: ' + tabDomain;
    console.log("Current URL:", tabURL);
    console.log("The hostname of URL:", tabDomain);
}

function extractDomain(url) {
    try {
        const parsedUrl = new URL(url);
        return parsedUrl.hostname;
    } catch (e) {
        return null;
    }
}



scanButton.addEventListener('click', handleScanClick);

