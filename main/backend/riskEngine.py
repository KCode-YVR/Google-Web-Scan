from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple
import json
import os

CONFIGDIR = os.path.join(os.path.dirname(__file__), "config")

def loadJsonList(filename: str) -> List[str]:
    path = os.path.join(CONFIGDIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    cleaned: List[str] = []
    for x in data:
        cleaned.append(str(x).strip())
    return cleaned

COMMONDOMAINS: Set[str] = set(loadJsonList("domains.json"))
TRUSTEDREGISTRARS: Set[str] = set(x.lower() for x in loadJsonList("registrar.json"))

def convertToUTC(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def daysBetween(earlier: datetime, later: datetime) -> int:
    return (later - earlier).days

def scoreCommonDomain(domain: str) -> Tuple[int, List[str]]:
    score_delta = 0
    reasons: List[str] = []

    if domain.lower() in COMMONDOMAINS:
        score_delta -= 60
        reasons.append("Domain name matched in top 100 most common domains searched")

    return score_delta, reasons


def scoreDomainAge(whoisData: Dict[str, Any], now: datetime) -> Tuple[int, List[str]]:
    score_delta = 0
    reasons: List[str] = []

    creationDate = convertToUTC(whoisData.get("creation_date"))
    if creationDate is None:
        score_delta += 15
        reasons.append("Domain missing creation date")
        return score_delta, reasons

    domainAgeDays = daysBetween(creationDate, now)  

    if domainAgeDays < 183:
        score_delta += 45
        reasons.append(f"Domain age is less than half a year: ({domainAgeDays} days old)")
    elif domainAgeDays <= 365:
        score_delta += 25
        reasons.append(f"Domain age is less than a year: ({domainAgeDays} days old)")
    else:
        score_delta -= 10
        reasons.append(f"Domain is over 1 year old: ({domainAgeDays} days old)")

    return score_delta, reasons


def scoreExpiration(whoisData: Dict[str, Any], now: datetime) -> Tuple[int, List[str]]:
    score_delta = 0
    reasons: List[str] = []

    expiration = convertToUTC(whoisData.get("expiration_date"))
    if expiration is None:
        score_delta += 15 
        reasons.append("Domain is missing an expiration date")
        return score_delta, reasons

    daysTillExpiration = daysBetween(now, expiration) 

    if daysTillExpiration < 0:
        score_delta += 40
        reasons.append(f"Domain is expired: ({abs(daysTillExpiration)} days ago)")
    elif daysTillExpiration < 31:
        score_delta += 30
        reasons.append(
            f"Domain expires within a month: ({daysTillExpiration} days until expiration)"
        )
    elif daysTillExpiration < 183:
        score_delta += 20
        reasons.append(
            f"Domain expires within half a year: ({daysTillExpiration} days until expiration)"
        )
    elif daysTillExpiration < 365:
        score_delta += 10
        reasons.append(
            f"Domain expires within this year: ({daysTillExpiration} days until expiration)"
        )
    else:
        score_delta -= 10
        reasons.append(
            f"Domain does not expire soon: ({daysTillExpiration} days until expiration)"
        )

    return score_delta, reasons


def scoreRegistrar(whoisData: Dict[str, Any]) -> Tuple[int, List[str]]:
    score_delta = 0
    reasons: List[str] = []

    registrar = whoisData.get("registrar")
    if not registrar:
        score_delta += 20
        reasons.append("Registrar missing or unavailable")
        return score_delta, reasons

    registrarNorm = str(registrar).strip().lower()

    if registrarNorm in TRUSTEDREGISTRARS:
        score_delta -= 20
        reasons.append("Registrar matches trusted registrar list")
    else:
        score_delta += 10
        reasons.append("Registrar is not found in trusted registrar list")

    return score_delta, reasons


def clampScore(score: int) -> int:
    return max(0, min(score, 100))


def classify(score: int) -> str:
    if score >= 70:
        return "unsafe"
    if score >= 30:
        return "be wary"
    return "safe"



def assessDomain(domain: str, whoisData: Dict[str, Any]) -> Dict[str, Any]:
    reasons: List[str] = []
    score = 0

    now = datetime.now(timezone.utc)

    delta, r = scoreCommonDomain(domain)
    score += delta
    reasons.extend(r)

    delta, r = scoreDomainAge(whoisData, now)
    score += delta
    reasons.extend(r)

    delta, r = scoreExpiration(whoisData, now)
    score += delta
    reasons.extend(r)

    delta, r = scoreRegistrar(whoisData)
    score += delta
    reasons.extend(r)
    
    score = clampScore(score)
    classification = classify(score)

    return {
        "domain": domain,
        "risk_score": score,
        "classification": classification,
        "reasons": reasons,
    }
