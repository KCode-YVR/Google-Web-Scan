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
        resultsDiv.innerHTML = 'Unable to read the current tab url.';
        return;
    }
    const tabURL = curTab.url;
    const tabDomain = extractDomain(curTab.url);
    if (!tabDomain) {
        resultsDiv.innerHTML = 'This page does not have a domain name.';
        return;
    }

    resultsDiv.innerHTML += `<br>Scanning domain, ${tabDomain}`;

    try {
        const result = await sendDomainToBackEnd(tabDomain);
        console.log("Backend response: ", result);
        resultsDiv.innerHTML += '<br>Scan complete.';
    } catch (e) {
        console.error(e);
        resultsDiv.innerHTML = 'Error with backend scan';
    }
}

function extractDomain(url) {
    try {
        const parsedUrl = new URL(url);
        return parsedUrl.hostname;
    } catch (e) {
        return null;
    }
}

async function sendDomainToBackEnd(domain) {
    const response = await fetch("http://localhost:8000/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            domain: domain
        })
    });
    return response.json();
}

scanButton.addEventListener('click', handleScanClick);

