import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from database import create_document, get_documents, db

app = FastAPI(title="moviQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "moviQ backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Schemas for incoming forms
class LeadIn(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    app: Literal['Uber','Bolt','FreeNow','Inna']
    preferred_model: Optional[str] = None

@app.post("/api/leads")
def create_lead(lead: LeadIn):
    try:
        lead_id = create_document("lead", lead.model_dump())
        return {"status": "ok", "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faq")
def get_faq():
    try:
        items = get_documents("faqitem", {}, 50)
        return items
    except Exception as e:
        # Return a default FAQ when db not available
        return [
            {"question": "Jak długo trwa procedura?", "answer": "Zwykle 1–3 dni robocze. Najszybciej – 24h."},
            {"question": "Czy mogę jeździć tylko na jednej aplikacji?", "answer": "Możesz korzystać z wielu aplikacji równocześnie."},
            {"question": "Co w przypadku kolizji?", "answer": "Zapewniamy pełne wsparcie, ubezpieczenie i auto zastępcze."},
        ]

@app.get("/api/vehicles")
def get_vehicles():
    try:
        cars = get_documents("vehicle", {}, 50)
        return cars
    except Exception:
        return [
            {"make": "Toyota", "model": "Corolla Hybrid", "price_monthly": 2499, "fuel": "hybryda", "photo_url": "https://images.unsplash.com/photo-1549923746-c502d488b3ea?q=80&w=1200&auto=format&fit=crop"},
            {"make": "Kia", "model": "Ceed", "price_monthly": 2199, "fuel": "benzyna", "photo_url": "https://images.unsplash.com/photo-1616788944660-a1189d712bb2?q=80&w=1200&auto=format&fit=crop"},
            {"make": "Hyundai", "model": "i30", "price_monthly": 2099, "fuel": "benzyna", "photo_url": "https://images.unsplash.com/photo-1619767886558-efdc259cde1b?q=80&w=1200&auto=format&fit=crop"},
            {"make": "Toyota", "model": "Yaris", "price_monthly": 1999, "fuel": "hybryda", "photo_url": "https://images.unsplash.com/photo-1581873372796-635b67ca200c?q=80&w=1200&auto=format&fit=crop"},
            {"make": "Skoda", "model": "Octavia", "price_monthly": 2699, "fuel": "benzyna", "photo_url": "https://images.unsplash.com/photo-1549922908-bdbb0370d0bf?q=80&w=1200&auto=format&fit=crop"},
        ]

@app.get("/api/pricing")
def get_pricing():
    try:
        plans = get_documents("pricingplan", {}, 10)
        return plans
    except Exception:
        return [
            {"name": "Standard", "price_from": 1999, "includes": ["Auto ekonomiczne", "Serwis i opony", "Ubezpieczenie"]},
            {"name": "Comfort", "price_from": 2399, "includes": ["Hybrydy", "Rozliczenia tyg./mies.", "Assistance 24/7"]},
            {"name": "Premium", "price_from": 2799, "includes": ["Większe auta", "Auto zastępcze", "Priorytetowy serwis"]},
        ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
