## Google-Web-Scan
# A simple WHOIS parser google extension.

This application offers the general public a quick, surface-level security check on any website by using a WHOIS parser. A WHOIS scan retrieves publicly available domain registration records, revealing key details such as the domain's creation date, the registrant's contact information, and name server data. Users can leverage this information to assess a site's reputation: a newly registered domain or inconsistent contact information can be a significant red flag, while a long-established domain and transparent registration details suggest legitimacy. The tool provides valuable transparency to help users quickly gauge the trustworthiness and history of a website.

This app is a google web extension which allow users to: 
- open the extension on their web browser
- run a whoois scanner to the current website that they are currently on the "scan" button
- view an assessment of the website which includes the domain name, the risk score provided by the program, a classification: "safe", "be wary", "unsafe", and the reasons to why it got the risk score
- view some of the whois data: creation date, expiration date, registrar, and name servers

Still being updated, adding a remote server soon!:) 

# Instructions:

The application currently only works if your local device hosts the server. To do so follow the following steps:
1. Clone this repository and save it to a local directory on your machine.
2. Open a terminal and navigate to the backend directory by using 'cd backend'
3. Install the required Python dependencies by using 'pip install -r requirements.txt'.
4. Start the FastAPI server by typing 'uvicorn main:app --reload'.
5. Open chrome and press 'manage extension'.
6. Make sure the developer mode is on.
7. Click 'Load unpacked' and select the file title 'extension'.  

``` mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API
    participant DB
    participant Cache

    User->>Browser: Enter credentials
    Browser->>API: POST /auth/login
    API->>DB: SELECT user WHERE email = ?
    DB-->>API: User record

    alt Invalid credentials
        API-->>Browser: 401 Unauthorized
        Browser-->>User: Show error message
    else Valid credentials
        API->>Cache: Store session token (TTL: 24h)
        Cache-->>API: OK
        API-->>Browser: 200 OK + JWT token
        Browser-->>User: Redirect to dashboard
    end

    Note over Browser,API: Subsequent authenticated requests

    User->>Browser: Visit protected page
    Browser->>API: GET /dashboard (Bearer token)
    API->>Cache: Validate token
    Cache-->>API: Token valid
    API-->>Browser: 200 OK + page data
    Browser-->>User: Render dashboard
```
