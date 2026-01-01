from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import whois

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=False,      
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan")
def scan(data: dict):
    domain = data.get("domain")
    return {"status": "received", "domain": domain}
