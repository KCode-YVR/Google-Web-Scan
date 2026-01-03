from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import os

CONFIGDIR = os.path.join(os.path.dirname(__file__), "config")

def loadJsonList(filename: str) -> List[str]:
    path = os.path.join(CONFIGDIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [str(x).strip() for x in data]
    
COMMONDOMAINS = set(loadJsonList("domains.json"))

TRUSTEDREGISTRARS = set(x.lower() for x in loadJsonList("registrar.json"))

def convertToUTC(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def differenceInDays(dateTime1: datetime, dateTime2: datetime) -> int:
    return (dateTime1-dateTime2).days

def assessDomain(domain: str, whoisData: Dict[str,Any]) -> Dict[str,Any]:
    reasons: List[str] = []
    score = 0

    now = datetime.now(timezone="utc")
    if domain.lower() in COMMONDOMAINS:
        score -= 100
        reasons.append("Domain name matched in top 100 most common domains searched")
    
    creationDate = convertToUTC(whoisData.get("creation_date"))
    if creationDate is None:
        score += 15
        reasons.append("Doomain missing creation date")
    else:
        domainAge = differenceInDays(creationDate, now)
        if domainAge < 183:
            score += 50
            reasons.append(f"Domain age is less than half a year: ({domainAge} days old)")
        elif domainAge <= 365:
            score += 25
            reasons.append(f"Domain age is less than a year: ({domainAge} days old)")
        else:
            score -= 10
            reasons.append(f"Domain is over 1 year old: ({domainAge} days old)")

    expiration = convertToUTC(whoisData.get("expiration_date"))
    if expiration is None:
        score += 20
        reasons.append("Domain is missing an expiration date")
    else:
        daysTillExpiration = differenceInDays(expiration, now)
        if daysTillExpiration < 0:
            score += 40
            reasons.append(f"Domain is expired: ({abs(daysTillExpiration)} days ago)")
        elif daysTillExpiration < 31:
            score += 30 
            reasons.append(f"Domain expires within a month: ({abs(daysTillExpiration)} days until expiration)")
        elif daysTillExpiration < 183:
            score += 20 
            reasons.append(f"Domain expires within half a year: ({abs(daysTillExpiration)} days until expiration)")
        elif daysTillExpiration < 365:
            score += 10 
            reasons.append(f"Domain expires within this year: ({abs(daysTillExpiration)} days until expiration)")
        else:
            score -= 10
            reasons.append(f"Domain does not expire soon: ({abs(daysTillExpiration)} days until expiration)")


    registrar = whoisData.get("registrar")
    if not registrar:
        score += 20
        reasons.append("Registrar missing or unavailable")
    else:
        registrarNorm = str(registrar).strip().lower()
        if registrarNorm in TRUSTEDREGISTRARS:
            score -= 20
            reasons.append("Registrar matches trusted registrar list")
        else:
            score += 10
            reasons.append("Registrar is not found in trusted registrar list")
    
    score = max(0, min(score, 100))
    if score >= 70:
        classification = "unsafe"
    elif score >= 30:
        classification = "be wary"
    else:
        classification = "safe"
    
    return {
        "domain": domain,
        "risk_score": score,
        "classification": classification,
        "reasons": reasons
    }