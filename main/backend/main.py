from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from whoisWrapper import lookUp
from riskEngine import assessDomain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=False,      
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
def scan(payload: dict):
    domain = payload.get("domain")
    if not domain or not isinstance(domain,str):
        raise HTTPException(status_code=400, detail="Missing or invalid domain")
    
    domain = domain.strip().lower()

    try:
        whoisData = lookUp(domain)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WHOIS lookup failed: {e}")
    
    assessment = assessDomain(domain, whoisData)

    return {
        "assessment": assessment,
        "whois": {
            "creation_date": str(whoisData.get("creation_date")),
            "expiration_date": str(whoisData.get("expiration_date")),
            "registrar": whoisData.get("registrar"),
            "name_servers": whoisData.get("name_servers"),
        }
    }
