from datetime import datetime
from typing import Any, Optional, List, Dict

import whois

def pickDate(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, List):
        validDate = []
        for v in value:
            if v is not None:
                validDate.append(v)
        if len(validDate) == 0:
            return None
        return min(validDate)
    if isinstance(value, datetime):
        return value
    return None

def lookUp(domain: str) -> Dict[str, Any]:
    w = whois.whois(domain)
    return {
        "domain": domain,
        "creation_date": pickDate(w.creation_date),
        "expiration_date": pickDate(w.expiration_date),
        "registrar": w.registrar,
        "name_servers": w.name_servers,
        "raw_text": w.text
    }