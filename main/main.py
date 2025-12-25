from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
