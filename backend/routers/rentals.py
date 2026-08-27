from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional, Union, Dict, Any
from datetime import datetime
from bson import ObjectId

from database import rentals_collection
from models import RentalCreate, RentalUpdate, RentalResponse
from routers.auth import get_current_user

router = APIRouter(prefix="/api/rentals", tags=["Rentals"])

def rental_helper(rental) -> dict:
    rental["_id"] = str(rental["_id"])
    return rental

@router.get("", response_model=List[RentalResponse])
async def get_rentals(
    status_filter: Optional[str] = Query(None, alias="status"),
    city_filter: Optional[str] = Query(None, alias="city"),
    wifi_filter: Optional[str] = Query(None, alias="wifiType"),
    search: Optional[str] = None
):
    query = {}
    if status_filter:
        query["status"] = status_filter
    if city_filter:
        query["city"] = city_filter
    if wifi_filter:
        query["wifiType"] = wifi_filter
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"city": {"$regex": search, "$options": "i"}},
            {"notes": {"$regex": search, "$options": "i"}},
            {"address": {"$regex": search, "$options": "i"}}
        ]

    cursor = rentals_collection.find(query).sort("updatedAt", -1)
    rentals = []
    async for doc in cursor:
        rentals.append(rental_helper(doc))
    return rentals

@router.post("", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
async def create_rental(
    rental_in: RentalCreate,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    now = datetime.utcnow()
    rental_dict = rental_in.model_dump()
    rental_dict["createdAt"] = now
    rental_dict["updatedAt"] = now
    
    if current_user:
        if isinstance(current_user, dict):
            rental_dict["owner_id"] = current_user.get("_id") or current_user.get("id")
        else:
            rental_dict["owner_id"] = getattr(current_user, "id", None) or getattr(current_user, "_id", None)

    res = await rentals_collection.insert_one(rental_dict)
    created = await rentals_collection.find_one({"_id": res.inserted_id})
    return rental_helper(created)

@router.get("/{rental_id}", response_model=RentalResponse)
async def get_rental(rental_id: str):
    if not ObjectId.is_valid(rental_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    rental = await rentals_collection.find_one({"_id": ObjectId(rental_id)})
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental_helper(rental)

@router.put("/{rental_id}", response_model=RentalResponse)
async def update_rental(
    rental_id: str,
    rental_in: RentalUpdate,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    if not ObjectId.is_valid(rental_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    update_data = {k: v for k, v in rental_in.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()

    res = await rentals_collection.find_one_and_update(
        {"_id": ObjectId(rental_id)},
        {"$set": update_data},
        return_document=True
    )
    if not res:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental_helper(res)

@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rental(
    rental_id: str,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    if not ObjectId.is_valid(rental_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    res = await rentals_collection.delete_one({"_id": ObjectId(rental_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rental not found")
    return None

@router.post("/seed", status_code=status.HTTP_201_CREATED)
async def seed_rentals():
    now = datetime.utcnow()
    sample_data = [
        {
            "title": "Bilocale Vista Mare vicino Stazione",
            "url": "https://www.subito.it",
            "platform": "Subito",
            "city": "Termoli",
            "address": "Via XXIV Maggio, Termoli",
            "monthlyPrice": 550.0,
            "utilities": "Incluse",
            "utilitiesPriceEstimate": 0.0,
            "condoFees": "Incluse",
            "condoFeesPriceEstimate": 0.0,
            "deposit": 550.0,
            "status": "Contattato",
            "wifiType": "Fibra FTTH",
            "workspaceType": "Scrivania dedicata",
            "parkingType": "Posto auto riservato",
            "ratingNeighborhood": 5,
            "ratingServices": 4,
            "ratingTransport": 5,
            "availablePeriod": "2 Mesi (Ottobre - Novembre)",
            "contactName": "Marco (Proprietario)",
            "contactPhone": "+39 333 1234567",
            "notes": "Molto disponibile. Ha confermato fibra 1Gbps e posto auto interno riservato.",
            "images": [
                "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&auto=format&fit=crop"
            ],
            "createdAt": now,
            "updatedAt": now
        },
        {
            "title": "Stanza Singola luminosa per studenti / lavoratori",
            "url": "https://www.idealista.it",
            "platform": "Idealista",
            "city": "Pescara",
            "address": "Viale Marconi, Pescara",
            "monthlyPrice": 320.0,
            "utilities": "A consumo",
            "utilitiesPriceEstimate": 40.0,
            "condoFees": "Incluse",
            "condoFeesPriceEstimate": 0.0,
            "deposit": 640.0,
            "status": "In Attesa",
            "wifiType": "Fibra FTTH",
            "workspaceType": "Scrivania dedicata",
            "parkingType": "Parcheggio libero in strada",
            "ratingNeighborhood": 4,
            "ratingServices": 5,
            "ratingTransport": 4,
            "availablePeriod": "10 Mesi (Anno Accademico)",
            "contactName": "Agenzia Immobiliare Pescara",
            "contactPhone": "+39 085 9876543",
            "notes": "Stanza ampia con scrivania e libreria. Contratto per studenti o lavoratori.",
            "images": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&auto=format&fit=crop"
            ],
            "createdAt": now,
            "updatedAt": now
        },
        {
            "title": "Bilocale moderno a 200m dalla spiaggia",
            "url": "https://www.facebook.com/marketplace",
            "platform": "Facebook",
            "city": "Termoli",
            "address": "Lungomare Cristoforo Colombo",
            "monthlyPrice": 480.0,
            "utilities": "Forfait",
            "utilitiesPriceEstimate": 50.0,
            "condoFees": "Incluse",
            "condoFeesPriceEstimate": 0.0,
            "deposit": 500.0,
            "status": "Visita/Videochiamata",
            "wifiType": "Wi-Fi da verificare",
            "workspaceType": "Scrivania dedicata",
            "parkingType": "Parcheggio libero in strada",
            "ratingNeighborhood": 5,
            "ratingServices": 3,
            "ratingTransport": 3,
            "availablePeriod": "6 Mesi (Semestre)",
            "contactName": "Lucia",
            "contactPhone": "+39 347 1122334",
            "notes": "Parcheggio gratuito sempre disponibile sotto casa.",
            "images": [
                "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600&auto=format&fit=crop"
            ],
            "createdAt": now,
            "updatedAt": now
        },
        {
            "title": "Monolocale moderno zona Pescara Centro",
            "url": "https://www.immobiliare.it",
            "platform": "Immobiliare",
            "city": "Pescara",
            "address": "Corso Umberto I",
            "monthlyPrice": 550.0,
            "utilities": "A consumo",
            "utilitiesPriceEstimate": 60.0,
            "condoFees": "Escluse",
            "condoFeesPriceEstimate": 30.0,
            "deposit": 550.0,
            "status": "Bozza",
            "wifiType": "FTTC",
            "workspaceType": "Tavolo grande",
            "parkingType": "Parcheggio a pagamento",
            "ratingNeighborhood": 4,
            "ratingServices": 5,
            "ratingTransport": 5,
            "availablePeriod": "12 Mesi (1 Anno)",
            "contactName": "Giovanni",
            "contactPhone": "",
            "notes": "Zona strisce blu. Verificare abbonamento mensile.",
            "images": [],
            "createdAt": now,
            "updatedAt": now
        }
    ]

    await rentals_collection.delete_many({})
    res = await rentals_collection.insert_many(sample_data)
    return {"message": f"Seeded {len(res.inserted_ids)} rentals successfully."}
