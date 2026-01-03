const scanButton = document.getElementById('scanButton');
const resultsDiv = document.getElementById('results');

async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
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
    const tabDomain = extractDomain(tabURL);
    if (!tabDomain) { 
        resultsDiv.innerHTML = 'This page does not have a domain name.';
        return;
    }

    resultsDiv.innerHTML += `<br>Scanning domain, ${tabDomain}`; 

    try {
        const result = await sendDomainToBackEnd(tabDomain); 
        console.log("Backend response: ", result);
        renderAssessment(result);
    } catch (e) {
        console.error(e);
        resultsDiv.innerHTML = 'Error with backend scan';
    }
}

function extractDomain(url) {
    try {
        return new URL(url).hostname;
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

function renderAssessment(result) {
    const assessment = result.assessment;
    const whois = result.whois;

    const reasonsHtml = assessment.reasons
        .map(r => `<li>${r}</li>`)
        .join("");

    resultsDiv.innerHTML = `
        <p><strong>Domain:</strong> ${assessment.domain}</p>
        <p><strong>Classification:</strong> ${assessment.classification}</p>
        <p><strong>Risk Score:</strong> ${assessment.risk_score}/100</p>

        <p><strong>Reasons:</strong></p>
        <ul>${reasonsHtml}</ul>

        <p><strong>WHOIS Summary:</strong></p>
        <p><strong>Creation:</strong> ${whois.creation_date}</p>
        <p><strong>Expiration:</strong> ${whois.expiration_date}</p>
        <p><strong>Registrar:</strong> ${whois.registrar}</p>
    `;
}

scanButton.addEventListener('click', handleScanClick);

